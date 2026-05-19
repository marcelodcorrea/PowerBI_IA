#!/usr/bin/env node
/**
 * PBIR Visual Editor - MCP Server (Node.js)
 * Edita visuais PBIR via Claude Code no VS Code
 * Compatível com PBIR formato 2.1.0:
 *   definition/pages/<hash>/page.json
 *   definition/pages/<hash>/visuals/<hash>/visual.json
 */

const readline = require('readline');
const fs = require('fs');
const path = require('path');

const REPORT_PATH = process.env.PBIP_REPORT_PATH || '';

// ==================== PBIR UTILS ====================

function getPagesDir(reportPath) {
  return path.join(reportPath, 'definition', 'pages');
}

function listPages(reportPath) {
  const pagesDir = getPagesDir(reportPath);
  const pagesMetaFile = path.join(pagesDir, 'pages.json');

  if (!fs.existsSync(pagesMetaFile)) {
    throw new Error(`pages.json não encontrado em: ${pagesDir}`);
  }

  const pagesMeta = JSON.parse(fs.readFileSync(pagesMetaFile, 'utf8'));
  const pageOrder = pagesMeta.pageOrder || [];

  const pages = [];
  for (const pageId of pageOrder) {
    const pageFile = path.join(pagesDir, pageId, 'page.json');
    if (fs.existsSync(pageFile)) {
      const pageData = JSON.parse(fs.readFileSync(pageFile, 'utf8'));
      const visualsDir = path.join(pagesDir, pageId, 'visuals');
      const visualCount = fs.existsSync(visualsDir)
        ? fs.readdirSync(visualsDir).filter(f =>
            fs.existsSync(path.join(visualsDir, f, 'visual.json'))).length
        : 0;

      pages.push({
        id: pageId,
        displayName: pageData.displayName || pageId,
        width: pageData.width,
        height: pageData.height,
        visualCount
      });
    }
  }
  return pages;
}

function findPage(reportPath, pageIdOrName) {
  const pages = listPages(reportPath);
  return pages.find(p => p.id === pageIdOrName || p.displayName === pageIdOrName) || null;
}

function getPageVisuals(reportPath, pageId) {
  const visualsDir = path.join(getPagesDir(reportPath), pageId, 'visuals');
  if (!fs.existsSync(visualsDir)) return [];

  const visuals = [];
  for (const visualId of fs.readdirSync(visualsDir)) {
    const visualFile = path.join(visualsDir, visualId, 'visual.json');
    if (fs.existsSync(visualFile)) {
      const d = JSON.parse(fs.readFileSync(visualFile, 'utf8'));
      visuals.push({
        id: visualId,
        displayName: d.name || visualId,
        type: d.visual?.visualType || d.visualType || 'unknown',
        x: d.position?.x ?? 0,
        y: d.position?.y ?? 0,
        width: d.position?.width ?? 0,
        height: d.position?.height ?? 0,
        isHidden: d.isHidden || false
      });
    }
  }
  return visuals;
}

function findVisual(reportPath, pageId, visualIdOrName) {
  const visualsDir = path.join(getPagesDir(reportPath), pageId, 'visuals');
  if (!fs.existsSync(visualsDir)) return null;

  for (const visualId of fs.readdirSync(visualsDir)) {
    const visualFile = path.join(visualsDir, visualId, 'visual.json');
    if (fs.existsSync(visualFile)) {
      const data = JSON.parse(fs.readFileSync(visualFile, 'utf8'));
      if (visualId === visualIdOrName || data.name === visualIdOrName) {
        return { id: visualId, file: visualFile, data };
      }
    }
  }
  return null;
}

function applyUpdates(data, updates) {
  if (updates.displayName !== undefined) data.name = updates.displayName;
  if (updates.isHidden !== undefined) data.isHidden = updates.isHidden;
  if (updates.x !== undefined || updates.y !== undefined ||
      updates.width !== undefined || updates.height !== undefined) {
    if (!data.position) data.position = {};
    if (updates.x !== undefined) data.position.x = updates.x;
    if (updates.y !== undefined) data.position.y = updates.y;
    if (updates.width !== undefined) data.position.width = updates.width;
    if (updates.height !== undefined) data.position.height = updates.height;
  }
  // Background color via visualContainerObjects (formato correto PBIR 2.8.0)
  if (updates.backgroundColor !== undefined) {
    if (!data.visual) data.visual = {};
    if (!data.visual.visualContainerObjects) data.visual.visualContainerObjects = {};
    data.visual.visualContainerObjects.background = [{
      properties: {
        color: { solid: { color: { expr: { Literal: { Value: `'${updates.backgroundColor}'` } } } } }
      }
    }];
  }
  // Permite patches arbitrários em qualquer propriedade via "raw"
  if (updates.raw) {
    Object.assign(data, updates.raw);
  }
  return data;
}

// ==================== TOOL HANDLERS ====================

function handleTool(name, args) {
  const reportPath = args.report_path || REPORT_PATH;
  if (!reportPath) throw new Error('report_path não informado e PBIP_REPORT_PATH não definido');
  if (!fs.existsSync(reportPath)) throw new Error(`Caminho não encontrado: ${reportPath}`);

  switch (name) {

    case 'get_summary': {
      const pages = listPages(reportPath);
      const summary = {};
      for (const page of pages) {
        summary[page.displayName] = getPageVisuals(reportPath, page.id);
      }
      const totalVisuals = Object.values(summary).reduce((a, v) => a + v.length, 0);
      return { success: true, pages_count: pages.length, total_visuals: totalVisuals, pages, summary };
    }

    case 'list_pages': {
      const pages = listPages(reportPath);
      return { success: true, count: pages.length, pages };
    }

    case 'get_page_visuals': {
      const page = findPage(reportPath, args.page);
      if (!page) throw new Error(`Página '${args.page}' não encontrada`);
      const visuals = getPageVisuals(reportPath, page.id);
      return { success: true, page: page.displayName, count: visuals.length, visuals };
    }

    case 'get_visual_structure': {
      const page = findPage(reportPath, args.page);
      if (!page) throw new Error(`Página '${args.page}' não encontrada`);
      const visual = findVisual(reportPath, page.id, args.visual);
      if (!visual) throw new Error(`Visual '${args.visual}' não encontrado na página '${page.displayName}'`);
      return { success: true, page: page.displayName, visualId: visual.id, structure: visual.data };
    }

    case 'update_visual': {
      const page = findPage(reportPath, args.page);
      if (!page) throw new Error(`Página '${args.page}' não encontrada`);
      const visual = findVisual(reportPath, page.id, args.visual);
      if (!visual) throw new Error(`Visual '${args.visual}' não encontrado na página '${page.displayName}'`);
      const updated = applyUpdates(visual.data, args.updates);
      fs.writeFileSync(visual.file, JSON.stringify(updated, null, 2), 'utf8');
      return { success: true, page: page.displayName, visualId: visual.id, applied: args.updates };
    }

    case 'batch_update': {
      const page = findPage(reportPath, args.page);
      if (!page) throw new Error(`Página '${args.page}' não encontrada`);
      const results = {};
      for (const item of args.updates) {
        try {
          const visual = findVisual(reportPath, page.id, item.visual);
          if (!visual) throw new Error(`Visual '${item.visual}' não encontrado`);
          const updated = applyUpdates(visual.data, item.changes);
          fs.writeFileSync(visual.file, JSON.stringify(updated, null, 2), 'utf8');
          results[item.visual] = { success: true };
        } catch (e) {
          results[item.visual] = { success: false, error: e.message };
        }
      }
      const succeeded = Object.values(results).filter(r => r.success).length;
      return { success: true, updated: succeeded, total: args.updates.length, results };
    }

    default:
      throw new Error(`Tool desconhecida: ${name}`);
  }
}

// ==================== MCP PROTOCOL ====================

const TOOLS = [
  {
    name: 'get_summary',
    description: 'Resumo de todas as páginas e visuais do relatório PBIR',
    inputSchema: { type: 'object', properties: { report_path: { type: 'string' } } }
  },
  {
    name: 'list_pages',
    description: 'Lista todas as páginas com metadados (id, displayName, dimensões, nº visuais)',
    inputSchema: { type: 'object', properties: { report_path: { type: 'string' } } }
  },
  {
    name: 'get_page_visuals',
    description: 'Lista visuais de uma página (id, nome, tipo, posição, tamanho, visibilidade)',
    inputSchema: {
      type: 'object', required: ['page'],
      properties: {
        page: { type: 'string', description: 'ID hash ou displayName da página' },
        report_path: { type: 'string' }
      }
    }
  },
  {
    name: 'get_visual_structure',
    description: 'Retorna JSON completo de um visual para inspecionar todas as propriedades',
    inputSchema: {
      type: 'object', required: ['page', 'visual'],
      properties: {
        page: { type: 'string' },
        visual: { type: 'string', description: 'ID hash ou nome do visual' },
        report_path: { type: 'string' }
      }
    }
  },
  {
    name: 'update_visual',
    description: 'Atualiza propriedades de um visual. Campos: displayName, x, y, width, height, isHidden, raw (objeto para patch arbitrário)',
    inputSchema: {
      type: 'object', required: ['page', 'visual', 'updates'],
      properties: {
        page: { type: 'string' },
        visual: { type: 'string' },
        updates: { type: 'object' },
        report_path: { type: 'string' }
      }
    }
  },
  {
    name: 'batch_update',
    description: 'Atualiza múltiplos visuais em uma página de uma só vez',
    inputSchema: {
      type: 'object', required: ['page', 'updates'],
      properties: {
        page: { type: 'string' },
        updates: {
          type: 'array',
          items: {
            type: 'object', required: ['visual', 'changes'],
            properties: {
              visual: { type: 'string' },
              changes: { type: 'object' }
            }
          }
        },
        report_path: { type: 'string' }
      }
    }
  }
];

const rl = readline.createInterface({ input: process.stdin, terminal: false });

function send(obj) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

rl.on('line', (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;

  let msg;
  try { msg = JSON.parse(trimmed); } catch { return; }

  const { id, method, params } = msg;

  if (method === 'initialize') {
    send({ jsonrpc: '2.0', id, result: {
      protocolVersion: '2024-11-05',
      capabilities: { tools: {} },
      serverInfo: { name: 'pbir-visual-editor', version: '1.0.0' }
    }});

  } else if (method === 'notifications/initialized') {
    // notificação — sem resposta

  } else if (method === 'tools/list') {
    send({ jsonrpc: '2.0', id, result: { tools: TOOLS } });

  } else if (method === 'tools/call') {
    let result;
    try {
      result = handleTool(params.name, params.arguments || {});
    } catch (e) {
      result = { success: false, error: e.message };
    }
    send({ jsonrpc: '2.0', id, result: {
      content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
    }});

  } else if (id !== undefined) {
    send({ jsonrpc: '2.0', id, error: { code: -32601, message: `Method not found: ${method}` } });
  }
});

process.stderr.write('[pbir-visual-editor] MCP Server iniciado\n');

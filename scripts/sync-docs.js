#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const repoRoot = path.resolve(__dirname, '..');
const docsRoot = path.join(repoRoot, 'docs');
const readmePath = path.join(docsRoot, 'README.md');
const sidebarPath = path.join(docsRoot, '_sidebar.md');

const readmeStart = '<!-- AUTO-GENERATED-INDEX:START -->';
const readmeEnd = '<!-- AUTO-GENERATED-INDEX:END -->';

const categoryOrder = [
  'AI',
  'CSS',
  'JS',
  'TypeScript',
  'React',
  '移动端',
  '工程化',
  'Eslint',
  'Vscode',
  '性能优化',
  '架构设计',
  '其他',
];

const categoryLabels = {
  AI: 'AI',
  CSS: 'CSS',
  JS: 'JavaScript',
  TypeScript: 'TypeScript',
  React: 'React',
  移动端: '移动端',
  工程化: '工程化',
  Eslint: 'Eslint',
  Vscode: 'VSCode',
  性能优化: '性能优化',
  架构设计: '架构设计',
  其他: '其他',
};

const excludedTopLevelDirs = new Set(['Images']);

function naturalCompare(a, b) {
  return a.localeCompare(b, 'zh-Hans-CN-u-co-pinyin', {
    numeric: true,
    sensitivity: 'base',
  });
}

function encodeDocsPath(relativePath) {
  return relativePath
    .split(path.sep)
    .map((segment) => segment.replace(/ /g, '%20'))
    .join('/');
}

function getArticleTitle(filePath, fileName) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split(/\r?\n/);

  for (const line of lines) {
    const trimmed = line.trim();

    if (!trimmed) {
      continue;
    }

    if (trimmed.startsWith('# ')) {
      return trimmed.slice(2).trim();
    }
  }

  return path.basename(fileName, '.md');
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function getCategoryWeight(name) {
  const index = categoryOrder.indexOf(name);
  return index === -1 ? Number.MAX_SAFE_INTEGER : index;
}

function getCategories() {
  const entries = fs
    .readdirSync(docsRoot, { withFileTypes: true })
    .filter(
      (entry) =>
        entry.isDirectory() &&
        !entry.name.startsWith('.') &&
        !excludedTopLevelDirs.has(entry.name),
    );

  const categories = entries
    .map((entry) => {
      const categoryDir = path.join(docsRoot, entry.name);
      const articles = fs
        .readdirSync(categoryDir, { withFileTypes: true })
        .filter((file) => file.isFile() && file.name.endsWith('.md'))
        .map((file) => {
          const filePath = path.join(categoryDir, file.name);
          const title = getArticleTitle(filePath, file.name);
          const relativePath = encodeDocsPath(path.join(entry.name, file.name));

          return {
            title,
            relativePath,
          };
        })
        .sort((a, b) => naturalCompare(a.title, b.title));

      return {
        key: entry.name,
        label: categoryLabels[entry.name] || entry.name,
        articles,
      };
    })
    .filter((category) => category.articles.length > 0)
    .sort((a, b) => {
      const weightDiff = getCategoryWeight(a.key) - getCategoryWeight(b.key);
      if (weightDiff !== 0) {
        return weightDiff;
      }

      return naturalCompare(a.label, b.label);
    });

  return categories;
}

function buildReadmeIndex(categories) {
  const total = categories.reduce(
    (sum, category) => sum + category.articles.length,
    0,
  );

  const lines = ['# 文章索引', '', `> 当前共 ${total} 篇文章，按分类整理如下。`, ''];

  for (const category of categories) {
    lines.push(`## ${category.label}（${category.articles.length}）`, '');

    for (const article of category.articles) {
      lines.push(`- [${article.title}](${article.relativePath})`);
    }

    lines.push('');
  }

  return lines.join('\n').trimEnd();
}

function buildSidebar(categories) {
  const lines = [
    '<!-- 该文件由 scripts/sync-docs.js 自动生成，请勿手动维护 -->',
    '',
    '- [首页](/)',
    '',
  ];

  for (const category of categories) {
    lines.push(`- ${category.label}`);

    for (const article of category.articles) {
      lines.push(`  - [${article.title}](${article.relativePath})`);
    }

    lines.push('');
  }

  return `${lines.join('\n').trimEnd()}\n`;
}

function syncReadme(indexContent) {
  const current = fs.readFileSync(readmePath, 'utf8');
  const replacement = `${readmeStart}\n${indexContent}\n${readmeEnd}`;
  const pattern = new RegExp(
    `${escapeRegExp(readmeStart)}[\\s\\S]*?${escapeRegExp(readmeEnd)}`,
  );

  let next = current;

  if (pattern.test(current)) {
    next = current.replace(pattern, replacement);
  } else {
    const indexHeading = current.indexOf('# 文章索引');
    const prefix =
      indexHeading === -1
        ? current.trimEnd()
        : current.slice(0, indexHeading).trimEnd();

    next = `${prefix}\n\n${replacement}\n`;
  }

  if (next !== current) {
    fs.writeFileSync(readmePath, next);
  }
}

function syncSidebar(sidebarContent) {
  const current = fs.existsSync(sidebarPath)
    ? fs.readFileSync(sidebarPath, 'utf8')
    : '';

  if (current !== sidebarContent) {
    fs.writeFileSync(sidebarPath, sidebarContent);
  }
}

function main() {
  const categories = getCategories();
  const indexContent = buildReadmeIndex(categories);
  const sidebarContent = buildSidebar(categories);
  const total = categories.reduce(
    (sum, category) => sum + category.articles.length,
    0,
  );

  syncReadme(indexContent);
  syncSidebar(sidebarContent);

  console.log(
    `Synced docs index and sidebar: ${categories.length} categories, ${total} articles.`,
  );
}

main();

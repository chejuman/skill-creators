#!/usr/bin/env python3
"""
Markdown to HTML Converter for Deep Researcher Reports
Converts research reports to visually appealing HTML with embedded styling.
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML-like frontmatter from markdown."""
    frontmatter = {}
    body = content

    if content.startswith('# '):
        # Extract title from first heading
        lines = content.split('\n')
        frontmatter['title'] = lines[0].replace('# ', '').strip()

    return frontmatter, body


def convert_tables(content: str) -> str:
    """Convert markdown tables to HTML tables."""
    lines = content.split('\n')
    result = []
    in_table = False
    table_lines = []

    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
        else:
            if in_table:
                result.append(process_table(table_lines))
                in_table = False
                table_lines = []
            result.append(line)

    if in_table:
        result.append(process_table(table_lines))

    return '\n'.join(result)


def process_table(lines: list) -> str:
    """Process table lines into HTML table."""
    if len(lines) < 2:
        return '\n'.join(lines)

    html = ['<div class="table-wrapper"><table>']

    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.split('|')[1:-1]]

        # Skip separator line
        if all(re.match(r'^[-:]+$', c) for c in cells):
            continue

        if i == 0:
            html.append('<thead><tr>')
            for cell in cells:
                html.append(f'<th>{convert_inline(cell)}</th>')
            html.append('</tr></thead><tbody>')
        else:
            html.append('<tr>')
            for cell in cells:
                html.append(f'<td>{convert_inline(cell)}</td>')
            html.append('</tr>')

    html.append('</tbody></table></div>')
    return '\n'.join(html)


def detect_chart_type(code: str) -> str:
    """Detect if code block contains ASCII chart and return type."""
    lines = code.strip().split('\n')

    # Timeline chart detection (contains year + progress bar)
    if any(re.search(r'20\d{2}.*[█▓░■]+', line) for line in lines):
        if any('타임라인' in line or '승인' in line or '인증' in line for line in lines):
            return 'timeline'

    # Growth chart detection (market size with CAGR)
    if 'CAGR' in code and any('■' in line for line in lines):
        if any(re.search(r'\$[\d.]+[BM]', line) for line in lines):
            return 'growth_chart'

    # Horizontal bar chart detection (percentage bars)
    if any(re.search(r'█+.*\d+%', line) for line in lines):
        return 'bar_chart'

    # Flow diagram detection (DeepCARS input/output)
    if '───' in code or '│' in code or '├' in code or '└' in code:
        if '입력' in code and '출력' in code and 'AI' in code:
            return 'flow_diagram'

    # Box diagram detection - must have box corners
    if '┌─' in code and '└─' in code:
        # Quarterly roadmap (has Q1-Q4)
        if any(re.search(r'Q[1-4]\s+20\d{2}', line) for line in lines):
            return 'quarterly_roadmap'

        # Process flow (has numbered stages with arrows)
        if any('▶' in line or '▼' in line for line in lines):
            if any(re.search(r'\d\.\s*(인식|평가|검증|선정|구축|확대|Awareness|Evaluation)', line) for line in lines):
                return 'process_flow'

        # Brand positioning (has before/after comparison)
        if '기존 포지셔닝' in code or '신규 포지셔닝' in code:
            return 'brand_positioning'

        # Segment priority (has priority levels with bars)
        if any('순위' in line for line in lines) and any('████' in line for line in lines):
            return 'segment_priority'

        # KOL/process diagram
        if 'KOL' in code or '식별' in code:
            return 'process_box'

        # GTM/Roadmap
        if 'Phase' in code or '로드맵' in code or '시장 진입' in code:
            return 'roadmap_box'

    # Competition positioning map (2D coordinate system)
    if '높은 전문화' in code or '낮은 전문화' in code:
        if '●' in code:
            return 'competition_map'

    return 'code'


def convert_timeline_chart(code: str) -> str:
    """Convert ASCII timeline to HTML timeline."""
    lines = code.strip().split('\n')
    items = []

    for line in lines:
        # Match pattern: YEAR  BARS TEXT STATUS
        match = re.search(r'(20\d{2}(?:\.\d{2})?(?:-\d{2})?)\s+([█▓░]+)\s*(.+?)(?:\s*([✓✅⏳🔜]))?$', line)
        if match:
            year = match.group(1)
            bar = match.group(2)
            text = match.group(3).strip()
            status = match.group(4) or ''

            # Determine status class
            if '█' in bar:
                status_class = 'completed'
                progress = 100
            elif '▓' in bar:
                status_class = 'in-progress'
                progress = 70
            else:
                status_class = 'planned'
                progress = 40

            items.append({
                'year': year,
                'text': text,
                'status': status,
                'status_class': status_class,
                'progress': progress
            })

    if not items:
        return None

    html = ['<div class="timeline-chart">']
    for item in items:
        html.append(f'''
        <div class="timeline-item {item['status_class']}">
            <div class="timeline-year">{item['year']}</div>
            <div class="timeline-content">
                <div class="timeline-bar" style="width: {item['progress']}%"></div>
                <div class="timeline-text">{item['text']} {item['status']}</div>
            </div>
        </div>''')
    html.append('</div>')

    return '\n'.join(html)


def convert_growth_chart(code: str) -> str:
    """Convert ASCII growth chart to HTML/SVG chart."""
    lines = code.strip().split('\n')

    # Extract metadata
    cagr = None
    years = []
    dollar_values = []
    bar_positions = []  # (row_index, column_position of first ■)

    for i, line in enumerate(lines):
        # Find CAGR
        cagr_match = re.search(r'CAGR\s+([\d.]+)%', line)
        if cagr_match:
            cagr = cagr_match.group(1)

        # Find dollar values
        value_match = re.search(r'\$([\d.]+)([BM])', line)
        if value_match:
            val = float(value_match.group(1))
            unit = value_match.group(2)
            dollar_values.append((val, unit))

        # Track ■ positions (column position indicates value height)
        if '■' in line:
            first_bar_pos = line.find('■')
            bar_positions.append((i, first_bar_pos))

        # Find years
        year_match = re.findall(r'20\d{2}', line)
        if year_match:
            years.extend(year_match)

    # Need at least 2 bar positions for a chart
    if len(bar_positions) < 2:
        return None

    # Sort dollar values to get start and end
    if dollar_values:
        dollar_values.sort(key=lambda x: x[0])
        start_value = dollar_values[0]
        end_value = dollar_values[-1]
    else:
        start_value = None
        end_value = None

    # Create data points from bar positions (higher column = higher value, but inverted in ASCII)
    # In ASCII, lower row number and higher column position = higher value
    data_points = [pos[1] for pos in bar_positions]  # column positions as relative values

    # Normalize data points for SVG
    max_val = max(data_points)
    min_val = min(data_points)
    normalized = [(p - min_val) / (max_val - min_val) * 80 + 10 if max_val != min_val else 50 for p in data_points]

    # Generate SVG path
    width = 400
    height = 200
    points = []
    for i, val in enumerate(normalized):
        x = 50 + (i / (len(normalized) - 1)) * (width - 100) if len(normalized) > 1 else width / 2
        y = height - 30 - (val / 100) * (height - 60)
        points.append(f"{x},{y}")

    path_d = "M " + " L ".join(points)

    # Create SVG
    start_label = f"${start_value[0]}{start_value[1]}" if start_value else ""
    end_label = f"${end_value[0]}{end_value[1]}" if end_value else ""
    cagr_label = f"CAGR {cagr}%" if cagr else ""

    html = f'''
    <div class="growth-chart">
        <svg viewBox="0 0 {width} {height}" class="chart-svg">
            <defs>
                <linearGradient id="chartGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
                </linearGradient>
            </defs>
            <!-- Grid lines -->
            <line x1="50" y1="30" x2="50" y2="{height-30}" stroke="#e5e7eb" stroke-width="1"/>
            <line x1="50" y1="{height-30}" x2="{width-50}" y2="{height-30}" stroke="#e5e7eb" stroke-width="1"/>
            <!-- Chart line -->
            <path d="{path_d}" fill="none" stroke="url(#chartGradient)" stroke-width="3" stroke-linecap="round"/>
            <!-- Data points -->'''

    for i, (x, y) in enumerate([(50 + (i / (len(normalized) - 1)) * (width - 100) if len(normalized) > 1 else width / 2,
                                  height - 30 - (normalized[i] / 100) * (height - 60)) for i in range(len(normalized))]):
        html += f'''
            <circle cx="{x}" cy="{y}" r="5" fill="#3b82f6"/>'''

    html += f'''
            <!-- Labels -->
            <text x="50" y="{height-10}" class="chart-label" text-anchor="middle">{years[0] if years else ''}</text>
            <text x="{width-50}" y="{height-10}" class="chart-label" text-anchor="middle">{years[-1] if years else ''}</text>
            <text x="30" y="{height-50}" class="chart-label" text-anchor="end" transform="rotate(-90, 30, {height-50})">{start_label}</text>
            <text x="{width-20}" y="50" class="chart-label">{end_label}</text>
        </svg>
        <div class="chart-cagr">{cagr_label}</div>
    </div>'''

    return html


def convert_bar_chart(code: str) -> str:
    """Convert ASCII horizontal bar chart to HTML."""
    lines = code.strip().split('\n')
    items = []

    for line in lines:
        # Match pattern: TEXT  BARS  PERCENTAGE
        match = re.search(r'([█▓░]+)\s*(\d+)%', line)
        if match:
            bar_length = len(match.group(1))
            percentage = int(match.group(2))

            # Extract label from line
            label_match = re.search(r'│\s*(.+?)\s*$', line.split('█')[0]) or re.search(r'^\s*(.+?)\s*█', line)
            label = label_match.group(1).strip() if label_match else f"Item {len(items)+1}"

            items.append({
                'label': label,
                'percentage': percentage
            })

    if not items:
        return None

    # Define colors
    colors = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b']

    html = ['<div class="bar-chart">']
    for i, item in enumerate(items):
        color = colors[i % len(colors)]
        html.append(f'''
        <div class="bar-item">
            <div class="bar-label">{item['label']}</div>
            <div class="bar-container">
                <div class="bar-fill" style="width: {item['percentage']}%; background: {color};">
                    <span class="bar-value">{item['percentage']}%</span>
                </div>
            </div>
        </div>''')
    html.append('</div>')

    return '\n'.join(html)


def convert_flow_diagram(code: str) -> str:
    """Convert ASCII flow diagram to HTML."""
    # For flow diagrams, we'll create a styled HTML version
    lines = code.strip().split('\n')

    # Detect if it's a simple input->process->output flow
    if '입력' in code and '출력' in code:
        # Extract components
        inputs = []
        outputs = []
        process = "AI 분석"

        for line in lines:
            if '혈압' in line or 'BP' in line:
                inputs.append('혈압 (BP)')
            if '심박수' in line or 'HR' in line:
                inputs.append('심박수 (HR)')
            if '호흡수' in line or 'RR' in line:
                inputs.append('호흡수 (RR)')
            if '체온' in line or 'Temp' in line:
                inputs.append('체온 (Temp)')
            if '위험도' in line:
                outputs.append('위험도 점수')
            if '24시간' in line or '예측' in line:
                outputs.append('24시간 예측')
            if 'RNN' in line or '딥러닝' in line:
                process = 'RNN 딥러닝'

        # Extract metrics
        metrics = []
        for line in lines:
            if 'AUROC' in line:
                match = re.search(r'AUROC[:\s]*([\d.-]+)', line)
                if match:
                    metrics.append(f"AUROC: {match.group(1)}")
            if '오경보' in line:
                match = re.search(r'([\d.]+)%', line)
                if match:
                    metrics.append(f"오경보 감소: {match.group(1)}%")

        html = f'''
        <div class="flow-diagram">
            <div class="flow-section flow-inputs">
                <div class="flow-title">입력 (4가지 활력징후)</div>
                <div class="flow-items">
                    {''.join(f'<div class="flow-item">{inp}</div>' for inp in inputs)}
                </div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-section flow-process">
                <div class="flow-title">AI 분석</div>
                <div class="flow-items">
                    <div class="flow-item process">{process}</div>
                </div>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-section flow-outputs">
                <div class="flow-title">출력</div>
                <div class="flow-items">
                    {''.join(f'<div class="flow-item">{out}</div>' for out in outputs)}
                </div>
            </div>
        </div>
        <div class="flow-metrics">
            {''.join(f'<span class="metric">{m}</span>' for m in metrics)}
        </div>'''

        return html

    return None


def convert_segment_priority(code: str) -> str:
    """Convert segment priority box to HTML."""
    lines = code.strip().split('\n')
    segments = []
    current_segment = None

    for line in lines:
        # Match priority line: "1순위: 상급종합병원 (500+ 병상)"
        priority_match = re.search(r'(\d)순위[:\s]+(.+?)(?:\s*\((.+?)\))?$', line.strip())
        if priority_match:
            if current_segment:
                segments.append(current_segment)
            current_segment = {
                'priority': int(priority_match.group(1)),
                'title': priority_match.group(2).strip(),
                'subtitle': priority_match.group(3) if priority_match.group(3) else '',
                'bar_width': 0,
                'description': '',
                'details': []
            }

        # Match bar line with description
        bar_match = re.search(r'(█+)\s*(.+)?$', line)
        if bar_match and current_segment:
            current_segment['bar_width'] = min(len(bar_match.group(1)) * 2, 100)
            if bar_match.group(2):
                current_segment['description'] = bar_match.group(2).strip()

        # Match detail line: "- 고위험 환자 집중"
        detail_match = re.search(r'[-▪]\s*(.+)$', line.strip())
        if detail_match and current_segment and not priority_match:
            current_segment['details'].append(detail_match.group(1))

    if current_segment:
        segments.append(current_segment)

    if not segments:
        return None

    # Extract title from first line
    title_match = re.search(r'│\s*(.+?세그먼트.+?|.+?우선순위.+?)\s*│', code)
    title = title_match.group(1).strip() if title_match else '타겟 세그먼트'

    colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b']

    html = [f'<div class="segment-priority"><div class="segment-title">{title}</div>']
    for seg in segments:
        color = colors[(seg['priority'] - 1) % len(colors)]
        html.append(f'''
        <div class="segment-item">
            <div class="segment-header">
                <span class="segment-rank" style="background: {color}">{seg['priority']}순위</span>
                <span class="segment-name">{seg['title']}</span>
                <span class="segment-subtitle">{seg['subtitle']}</span>
            </div>
            <div class="segment-bar-container">
                <div class="segment-bar" style="width: {seg['bar_width']}%; background: {color}"></div>
                <span class="segment-desc">{seg['description']}</span>
            </div>
            <ul class="segment-details">
                {''.join(f'<li>{d}</li>' for d in seg['details'])}
            </ul>
        </div>''')
    html.append('</div>')
    return '\n'.join(html)


def convert_process_flow(code: str) -> str:
    """Convert buyer journey / process flow diagram to HTML."""
    lines = code.strip().split('\n')
    stages = []
    current_stage = None

    for line in lines:
        # Match stage header: "1. 인식 (Awareness)"
        stage_match = re.search(r'(\d)\.\s*(.+?)\s*(?:\((.+?)\))?(?:\s*$|\s+\d\.)', line)
        if stage_match:
            if current_stage:
                stages.append(current_stage)
            current_stage = {
                'number': int(stage_match.group(1)),
                'title_ko': stage_match.group(2).strip(),
                'title_en': stage_match.group(3) if stage_match.group(3) else '',
                'items': []
            }

        # Match item: "▪ 컨퍼런스 참석"
        item_match = re.search(r'[▪•]\s*(.+?)(?:\s*│|$)', line)
        if item_match and current_stage:
            item = item_match.group(1).strip()
            if item and len(item) > 1:
                current_stage['items'].append(item)

    if current_stage:
        stages.append(current_stage)

    if not stages:
        return None

    # Extract title
    title_match = re.search(r'│\s*(.+?결정.+?|.+?Journey.+?|.+?과정.+?)\s*│', code)
    title = title_match.group(1).strip() if title_match else '프로세스 플로우'

    # Extract footer info
    footer_items = []
    for line in lines:
        if '평균' in line or '핵심' in line or '성공' in line:
            match = re.search(r'([^│]+(?:평균|핵심|성공)[^│]+)', line)
            if match:
                footer_items.append(match.group(1).strip())

    colors = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']

    html = [f'<div class="process-flow"><div class="process-title">{title}</div><div class="process-stages">']
    for i, stage in enumerate(stages):
        color = colors[i % len(colors)]
        html.append(f'''
        <div class="process-stage">
            <div class="stage-header" style="border-color: {color}">
                <span class="stage-number" style="background: {color}">{stage['number']}</span>
                <span class="stage-title">{stage['title_ko']}</span>
                <span class="stage-subtitle">{stage['title_en']}</span>
            </div>
            <ul class="stage-items">
                {''.join(f'<li>{item}</li>' for item in stage['items'])}
            </ul>
        </div>''')
        if i < len(stages) - 1:
            html.append('<div class="process-arrow">→</div>')
    html.append('</div>')
    if footer_items:
        html.append(f'<div class="process-footer">{"<br>".join(footer_items)}</div>')
    html.append('</div>')
    return '\n'.join(html)


def convert_quarterly_roadmap(code: str) -> str:
    """Convert quarterly roadmap to HTML."""
    lines = code.strip().split('\n')
    quarters = []
    current_quarter = None

    for line in lines:
        # Match quarter header: "Q1 2025 (1-3월)"
        quarter_match = re.search(r'(Q[1-4])\s+(20\d{2})(?:\s*\((.+?)\))?', line)
        if quarter_match:
            if current_quarter:
                quarters.append(current_quarter)
            current_quarter = {
                'quarter': quarter_match.group(1),
                'year': quarter_match.group(2),
                'period': quarter_match.group(3) if quarter_match.group(3) else '',
                'items': [],
                'kpi': ''
            }

        # Match item: "▪ Clinical Advisory Board 구성"
        item_match = re.search(r'[▪•]\s*(.+?)(?:\s*│|$)', line)
        if item_match and current_quarter:
            item = item_match.group(1).strip()
            if item and len(item) > 1:
                if 'KPI' in item:
                    current_quarter['kpi'] = item.replace('KPI:', '').strip()
                else:
                    current_quarter['items'].append(item)

    if current_quarter:
        quarters.append(current_quarter)

    if not quarters:
        return None

    # Extract title
    title_match = re.search(r'│\s*(.+?계획.+?|.+?실행.+?|.+?마일스톤.+?)\s*│', code)
    title = title_match.group(1).strip() if title_match else '실행 로드맵'

    colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b']

    html = [f'<div class="quarterly-roadmap"><div class="roadmap-title">{title}</div><div class="roadmap-quarters">']
    for i, q in enumerate(quarters):
        color = colors[i % len(colors)]
        html.append(f'''
        <div class="quarter-card">
            <div class="quarter-header" style="background: {color}">
                <span class="quarter-name">{q['quarter']} {q['year']}</span>
                <span class="quarter-period">{q['period']}</span>
            </div>
            <ul class="quarter-items">
                {''.join(f'<li>{item}</li>' for item in q['items'])}
            </ul>
            {f'<div class="quarter-kpi"><strong>KPI:</strong> {q["kpi"]}</div>' if q['kpi'] else ''}
        </div>''')
    html.append('</div></div>')
    return '\n'.join(html)


def convert_brand_positioning(code: str) -> str:
    """Convert brand positioning box to HTML."""
    lines = code.strip().split('\n')

    old_pos = ''
    new_pos = ''
    reasons = []
    message = ''

    for line in lines:
        if '기존 포지셔닝' in line or 'AI 기반' in line:
            match = re.search(r'"(.+?)"', line)
            if match:
                old_pos = match.group(1)
        if '신규 포지셔닝' in line or 'Alarm Fatigue' in line or 'The' in line:
            match = re.search(r'"(.+?)"', line)
            if match:
                new_pos = match.group(1)
        if line.strip().startswith('✓'):
            reasons.append(line.strip()[1:].strip())
        if '핵심 메시지' in code and ('fewer' in line.lower() or 'alarm' in line.lower()):
            msg_match = re.search(r'"(.+?)"', line)
            if msg_match:
                message = msg_match.group(1)

    if not old_pos and not new_pos:
        return None

    html = f'''
    <div class="brand-positioning">
        <div class="positioning-comparison">
            <div class="positioning-old">
                <div class="positioning-label">기존 포지셔닝</div>
                <div class="positioning-text">{old_pos or "AI 기반 심정지 예측 솔루션"}</div>
            </div>
            <div class="positioning-arrow">→</div>
            <div class="positioning-new">
                <div class="positioning-label">신규 포지셔닝</div>
                <div class="positioning-text">{new_pos or "The Alarm Fatigue Solution"}</div>
            </div>
        </div>
        <div class="positioning-reasons">
            <div class="reasons-title">왜 이 포지셔닝인가?</div>
            <ul>
                {''.join(f'<li><span class="check">✓</span> {r}</li>' for r in reasons)}
            </ul>
        </div>
        {f'<div class="positioning-message"><strong>핵심 메시지:</strong> "{message}"</div>' if message else ''}
    </div>'''
    return html


def convert_competition_map(code: str) -> str:
    """Convert competition positioning map to HTML."""
    lines = code.strip().split('\n')
    companies = []

    for line in lines:
        # Match company with position marker: "DeepCARS ●─────"
        company_match = re.search(r'(\w+(?:\.\w+)?)\s*●[─]*\s*(.+)?', line)
        if company_match:
            companies.append({
                'name': company_match.group(1),
                'description': company_match.group(2).strip() if company_match.group(2) else ''
            })

    if not companies:
        return None

    # Define positions based on original chart
    positions = {
        'DeepCARS': {'x': 25, 'y': 20, 'color': '#3b82f6', 'desc': '심정지 예측 특화'},
        'JLK': {'x': 60, 'y': 35, 'color': '#8b5cf6', 'desc': '뇌졸중 특화'},
        'Aidoc': {'x': 75, 'y': 55, 'color': '#06b6d4', 'desc': '방사선 플랫폼'},
        'Viz': {'x': 80, 'y': 65, 'color': '#10b981', 'desc': '응급신경과'},
        'Lunit': {'x': 35, 'y': 85, 'color': '#f59e0b', 'desc': '암 진단 영상'}
    }

    html = '''
    <div class="competition-map">
        <div class="map-title">경쟁 포지셔닝 맵</div>
        <div class="map-container">
            <div class="map-axis-y">
                <span class="axis-label top">높은 전문화</span>
                <span class="axis-label bottom">낮은 전문화</span>
            </div>
            <div class="map-grid">
                <div class="map-axis-x">
                    <span class="axis-label left">좁은 시장</span>
                    <span class="axis-label right">넓은 시장</span>
                </div>'''

    for company in companies:
        name = company['name']
        if name in positions:
            pos = positions[name]
            html += f'''
                <div class="map-point" style="left: {pos['x']}%; top: {pos['y']}%;">
                    <div class="point-marker" style="background: {pos['color']}"></div>
                    <div class="point-label" style="color: {pos['color']}">{name}</div>
                    <div class="point-desc">{pos['desc']}</div>
                </div>'''

    html += '''
            </div>
        </div>
    </div>'''
    return html


def convert_generic_box(code: str, title_hint: str = '') -> str:
    """Convert generic box diagram to styled HTML card."""
    lines = code.strip().split('\n')

    # Extract title from header
    title = title_hint
    for line in lines:
        if '│' in line and not line.strip().startswith('│'):
            continue
        title_match = re.search(r'│\s*(.{5,50}?)\s*│', line)
        if title_match and not title:
            candidate = title_match.group(1).strip()
            if len(candidate) > 3 and '─' not in candidate and '┌' not in candidate:
                title = candidate
                break

    # Extract content items
    items = []
    for line in lines:
        if '▪' in line or '•' in line or '✓' in line:
            match = re.search(r'[▪•✓]\s*(.+?)(?:\s*│|$)', line)
            if match:
                items.append(match.group(1).strip())
        elif '───▶' in line or '→' in line:
            # Skip arrow lines
            continue

    if not items and not title:
        return None

    html = f'''
    <div class="info-box">
        <div class="info-box-title">{title}</div>
        <ul class="info-box-items">
            {''.join(f'<li>{item}</li>' for item in items)}
        </ul>
    </div>'''
    return html


def convert_code_blocks(content: str) -> str:
    """Convert fenced code blocks to HTML, with special handling for ASCII charts."""
    pattern = r'```(\w*)\n(.*?)```'

    def replacer(match):
        lang = match.group(1) or 'text'
        code = match.group(2).rstrip()

        # Detect and convert ASCII charts
        chart_type = detect_chart_type(code)

        if chart_type == 'timeline':
            html = convert_timeline_chart(code)
            if html:
                return html

        elif chart_type == 'growth_chart':
            html = convert_growth_chart(code)
            if html:
                return html

        elif chart_type == 'bar_chart':
            html = convert_bar_chart(code)
            if html:
                return html

        elif chart_type == 'flow_diagram':
            html = convert_flow_diagram(code)
            if html:
                return html

        elif chart_type == 'segment_priority':
            html = convert_segment_priority(code)
            if html:
                return html

        elif chart_type == 'process_flow':
            html = convert_process_flow(code)
            if html:
                return html

        elif chart_type == 'quarterly_roadmap':
            html = convert_quarterly_roadmap(code)
            if html:
                return html

        elif chart_type == 'brand_positioning':
            html = convert_brand_positioning(code)
            if html:
                return html

        elif chart_type == 'competition_map':
            html = convert_competition_map(code)
            if html:
                return html

        elif chart_type in ('process_box', 'roadmap_box'):
            html = convert_generic_box(code)
            if html:
                return html

        # Default: escape HTML and return as code block
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre class="code-block" data-lang="{lang}"><code>{code}</code></pre>'

    return re.sub(pattern, replacer, content, flags=re.DOTALL)


def convert_inline(text: str) -> str:
    """Convert inline markdown elements."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code class="inline-code">\1</code>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', text)
    # Checkmarks and emojis
    text = text.replace('✓', '<span class="check">✓</span>')
    text = text.replace('✅', '<span class="check">✅</span>')
    text = text.replace('⏳', '<span class="pending">⏳</span>')

    return text


def convert_headings(content: str) -> str:
    """Convert markdown headings to HTML with anchors."""
    lines = content.split('\n')
    result = []

    for line in lines:
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2)
            anchor = re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')
            result.append(f'<h{level} id="{anchor}">{convert_inline(text)}</h{level}>')
        else:
            result.append(line)

    return '\n'.join(result)


def convert_lists(content: str) -> str:
    """Convert markdown lists to HTML."""
    lines = content.split('\n')
    result = []
    in_list = False
    list_type = None

    for line in lines:
        # Ordered list
        ol_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        # Unordered list
        ul_match = re.match(r'^[-*]\s+(.+)$', line)

        if ol_match:
            if not in_list or list_type != 'ol':
                if in_list:
                    result.append(f'</{list_type}>')
                result.append('<ol>')
                in_list = True
                list_type = 'ol'
            result.append(f'<li>{convert_inline(ol_match.group(2))}</li>')
        elif ul_match:
            if not in_list or list_type != 'ul':
                if in_list:
                    result.append(f'</{list_type}>')
                result.append('<ul>')
                in_list = True
                list_type = 'ul'
            result.append(f'<li>{convert_inline(ul_match.group(1))}</li>')
        else:
            if in_list and line.strip() == '':
                result.append(f'</{list_type}>')
                in_list = False
                list_type = None
            result.append(line)

    if in_list:
        result.append(f'</{list_type}>')

    return '\n'.join(result)


def convert_paragraphs(content: str) -> str:
    """Convert text blocks to paragraphs."""
    lines = content.split('\n')
    result = []
    paragraph = []

    for line in lines:
        if line.strip() == '':
            if paragraph:
                text = ' '.join(paragraph)
                if not text.startswith('<'):
                    result.append(f'<p>{convert_inline(text)}</p>')
                else:
                    result.append(text)
                paragraph = []
            result.append('')
        elif line.startswith('<') or line.startswith('#'):
            if paragraph:
                text = ' '.join(paragraph)
                if not text.startswith('<'):
                    result.append(f'<p>{convert_inline(text)}</p>')
                else:
                    result.append(text)
                paragraph = []
            result.append(line)
        else:
            paragraph.append(line)

    if paragraph:
        text = ' '.join(paragraph)
        if not text.startswith('<'):
            result.append(f'<p>{convert_inline(text)}</p>')
        else:
            result.append(text)

    return '\n'.join(result)


def extract_toc(content: str) -> str:
    """Extract table of contents from headings."""
    toc = ['<nav class="toc"><h3>목차</h3><ul>']

    for match in re.finditer(r'^(#{2,3})\s+(.+)$', content, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2)
        anchor = re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')
        indent = 'toc-h3' if level == 3 else ''
        toc.append(f'<li class="{indent}"><a href="#{anchor}">{text}</a></li>')

    toc.append('</ul></nav>')
    return '\n'.join(toc)


def apply_inline_to_text(content: str) -> str:
    """Apply inline markdown conversion to non-HTML text lines."""
    lines = content.split('\n')
    result = []

    for line in lines:
        # Skip lines that are already HTML tags or code blocks
        stripped = line.strip()
        if (stripped.startswith('<') or
            stripped.startswith('```') or
            '<pre' in line or
            '<code>' in line):
            result.append(line)
        else:
            # Apply inline conversions to regular text
            result.append(convert_inline(line))

    return '\n'.join(result)


def md_to_html(md_content: str, title: str = "Research Report") -> str:
    """Convert markdown to complete HTML document."""

    # Extract frontmatter
    frontmatter, body = parse_frontmatter(md_content)
    if 'title' in frontmatter:
        title = frontmatter['title']

    # Generate TOC
    toc = extract_toc(body)

    # Convert markdown elements (order matters)
    html_body = body
    html_body = convert_code_blocks(html_body)
    html_body = convert_tables(html_body)
    html_body = convert_headings(html_body)
    html_body = convert_lists(html_body)
    # Apply inline markdown (bold, italic, links) to remaining text
    html_body = apply_inline_to_text(html_body)

    # Build final HTML
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{get_styles()}
    </style>
</head>
<body>
    <div class="container">
        <aside class="sidebar">
            {toc}
        </aside>
        <main class="content">
            <article>
{html_body}
            </article>
        </main>
    </div>
    <script>
{get_scripts()}
    </script>
</body>
</html>'''

    return html


def get_styles() -> str:
    """Return embedded CSS styles."""
    return '''
:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary: #64748b;
    --success: #22c55e;
    --warning: #f59e0b;
    --danger: #ef4444;
    --bg: #f8fafc;
    --bg-card: #ffffff;
    --text: #1e293b;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --code-bg: #1e293b;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    font-size: 16px;
}

.container {
    display: flex;
    max-width: 1400px;
    margin: 0 auto;
    min-height: 100vh;
}

.sidebar {
    width: 280px;
    background: var(--bg-card);
    border-right: 1px solid var(--border);
    padding: 2rem 1.5rem;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
}

.toc h3 {
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 1rem;
}

.toc ul {
    list-style: none;
}

.toc li {
    margin-bottom: 0.5rem;
}

.toc a {
    color: var(--text);
    text-decoration: none;
    font-size: 0.9rem;
    display: block;
    padding: 0.25rem 0;
    border-left: 2px solid transparent;
    padding-left: 0.75rem;
    transition: all 0.2s;
}

.toc a:hover {
    color: var(--primary);
    border-left-color: var(--primary);
}

.toc .toc-h3 {
    padding-left: 1.5rem;
}

.content {
    flex: 1;
    padding: 3rem 4rem;
    max-width: 900px;
}

article {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 3rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--text);
    border-bottom: 3px solid var(--primary);
    padding-bottom: 1rem;
}

h2 {
    font-size: 1.75rem;
    font-weight: 600;
    margin: 3rem 0 1.5rem;
    color: var(--text);
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
}

h3 {
    font-size: 1.35rem;
    font-weight: 600;
    margin: 2rem 0 1rem;
    color: var(--text);
}

h4 {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 1.5rem 0 0.75rem;
    color: var(--secondary);
}

p {
    margin-bottom: 1rem;
}

a {
    color: var(--primary);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

strong {
    font-weight: 600;
    color: var(--text);
}

.table-wrapper {
    overflow-x: auto;
    margin: 1.5rem 0;
    border-radius: 8px;
    border: 1px solid var(--border);
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}

thead {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
}

th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
}

td {
    padding: 0.875rem 1rem;
    border-bottom: 1px solid var(--border);
}

tbody tr:hover {
    background: var(--bg);
}

tbody tr:last-child td {
    border-bottom: none;
}

.code-block {
    background: var(--code-bg);
    color: #e2e8f0;
    padding: 1.5rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1.5rem 0;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 0.875rem;
    line-height: 1.6;
    position: relative;
}

.code-block::before {
    content: attr(data-lang);
    position: absolute;
    top: 0.5rem;
    right: 1rem;
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
}

.inline-code {
    background: #f1f5f9;
    color: var(--primary-dark);
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875em;
}

ul, ol {
    margin: 1rem 0 1.5rem 1.5rem;
}

li {
    margin-bottom: 0.5rem;
}

.check {
    color: var(--success);
    font-weight: bold;
}

.pending {
    color: var(--warning);
}

hr {
    border: none;
    border-top: 2px solid var(--border);
    margin: 3rem 0;
}

blockquote {
    border-left: 4px solid var(--primary);
    padding-left: 1.5rem;
    margin: 1.5rem 0;
    color: var(--text-muted);
    font-style: italic;
}

/* Responsive */
@media (max-width: 1024px) {
    .sidebar {
        display: none;
    }

    .content {
        padding: 2rem;
    }
}

@media (max-width: 640px) {
    .content {
        padding: 1rem;
    }

    article {
        padding: 1.5rem;
    }

    h1 {
        font-size: 1.75rem;
    }

    h2 {
        font-size: 1.35rem;
    }
}

/* Print styles */
@media print {
    .sidebar {
        display: none;
    }

    .content {
        max-width: 100%;
        padding: 0;
    }

    article {
        box-shadow: none;
    }
}

/* === Chart Visualization Styles === */

/* Timeline Chart */
.timeline-chart {
    margin: 2rem 0;
    padding: 1.5rem;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 12px;
    border: 1px solid var(--border);
}

.timeline-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
    padding: 0.75rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s, box-shadow 0.2s;
}

.timeline-item:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.timeline-item:last-child {
    margin-bottom: 0;
}

.timeline-year {
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--primary);
    min-width: 80px;
    padding: 0.25rem 0.5rem;
    background: #eff6ff;
    border-radius: 4px;
    text-align: center;
}

.timeline-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.timeline-bar {
    height: 8px;
    background: linear-gradient(90deg, var(--primary) 0%, #8b5cf6 100%);
    border-radius: 4px;
    transition: width 0.5s ease-out;
}

.timeline-item.completed .timeline-bar {
    background: linear-gradient(90deg, var(--success) 0%, #16a34a 100%);
}

.timeline-item.in-progress .timeline-bar {
    background: linear-gradient(90deg, var(--warning) 0%, #d97706 100%);
}

.timeline-item.planned .timeline-bar {
    background: linear-gradient(90deg, #94a3b8 0%, #64748b 100%);
}

.timeline-text {
    font-size: 0.9rem;
    color: var(--text);
}

/* Growth Chart (SVG) */
.growth-chart {
    margin: 2rem 0;
    padding: 1.5rem;
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chart-svg {
    width: 100%;
    max-width: 500px;
    height: auto;
    display: block;
    margin: 0 auto;
}

.chart-svg text {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 12px;
    fill: var(--text-muted);
}

.chart-svg .chart-label {
    font-size: 11px;
    fill: var(--secondary);
}

.chart-cagr {
    text-align: center;
    margin-top: 1rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary);
    background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    display: inline-block;
    margin-left: 50%;
    transform: translateX(-50%);
}

/* Bar Chart */
.bar-chart {
    margin: 2rem 0;
    padding: 1.5rem;
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.bar-item {
    margin-bottom: 1rem;
}

.bar-item:last-child {
    margin-bottom: 0;
}

.bar-label {
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 0.5rem;
}

.bar-container {
    height: 32px;
    background: #f1f5f9;
    border-radius: 6px;
    overflow: hidden;
    position: relative;
}

.bar-fill {
    height: 100%;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 0.75rem;
    transition: width 0.6s ease-out;
    min-width: 60px;
}

.bar-value {
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* Flow Diagram */
.flow-diagram {
    display: flex;
    align-items: stretch;
    justify-content: center;
    gap: 0.5rem;
    margin: 2rem 0;
    padding: 2rem;
    background: linear-gradient(135deg, #f8fafc 0%, #f0f9ff 100%);
    border-radius: 12px;
    border: 1px solid var(--border);
    flex-wrap: wrap;
}

.flow-section {
    flex: 1;
    min-width: 150px;
    max-width: 200px;
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 2px solid transparent;
    transition: all 0.3s;
}

.flow-section:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.flow-inputs {
    border-color: #3b82f6;
    background: linear-gradient(135deg, #eff6ff 0%, white 100%);
}

.flow-process {
    border-color: #8b5cf6;
    background: linear-gradient(135deg, #f5f3ff 0%, white 100%);
}

.flow-outputs {
    border-color: #10b981;
    background: linear-gradient(135deg, #ecfdf5 0%, white 100%);
}

.flow-title {
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
}

.flow-inputs .flow-title { color: #3b82f6; }
.flow-process .flow-title { color: #8b5cf6; }
.flow-outputs .flow-title { color: #10b981; }

.flow-items {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.flow-item {
    font-size: 0.85rem;
    padding: 0.5rem 0.75rem;
    background: #f8fafc;
    border-radius: 6px;
    color: var(--text);
}

.flow-item.process {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    color: white;
    font-weight: 600;
    text-align: center;
}

.flow-arrow {
    display: flex;
    align-items: center;
    font-size: 2rem;
    color: var(--primary);
    padding: 0 0.5rem;
    opacity: 0.6;
}

.flow-metrics {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.metric {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: white;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--primary);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--border);
}

/* Responsive chart styles */
@media (max-width: 768px) {
    .flow-diagram {
        flex-direction: column;
        align-items: center;
    }

    .flow-section {
        max-width: 100%;
        width: 100%;
    }

    .flow-arrow {
        transform: rotate(90deg);
        padding: 0.5rem 0;
    }

    .timeline-item {
        flex-direction: column;
        align-items: flex-start;
    }

    .timeline-year {
        min-width: auto;
    }

    .growth-chart {
        padding: 1rem;
    }
}

/* === Additional Chart Styles === */

/* Segment Priority */
.segment-priority {
    margin: 2rem 0;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.segment-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1.5rem;
    text-align: center;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--border);
}

.segment-item {
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: #f8fafc;
    border-radius: 8px;
}

.segment-item:last-child {
    margin-bottom: 0;
}

.segment-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}

.segment-rank {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    color: white;
    font-weight: 600;
    font-size: 0.85rem;
}

.segment-name {
    font-weight: 600;
    color: var(--text);
}

.segment-subtitle {
    color: var(--text-muted);
    font-size: 0.9rem;
}

.segment-bar-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.75rem;
}

.segment-bar {
    height: 8px;
    border-radius: 4px;
    transition: width 0.5s ease-out;
}

.segment-desc {
    font-size: 0.85rem;
    color: var(--text-muted);
    font-weight: 500;
}

.segment-details {
    list-style: none;
    margin: 0;
    padding-left: 0;
}

.segment-details li {
    font-size: 0.85rem;
    color: var(--secondary);
    margin-bottom: 0.25rem;
    padding-left: 1rem;
    position: relative;
}

.segment-details li::before {
    content: "•";
    position: absolute;
    left: 0;
    color: var(--primary);
}

/* Process Flow */
.process-flow {
    margin: 2rem 0;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.process-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1.5rem;
    text-align: center;
}

.process-stages {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    justify-content: center;
    gap: 0.5rem;
}

.process-stage {
    flex: 1;
    min-width: 140px;
    max-width: 180px;
    background: #f8fafc;
    border-radius: 8px;
    padding: 1rem;
}

.stage-header {
    border-left: 3px solid;
    padding-left: 0.75rem;
    margin-bottom: 0.75rem;
}

.stage-number {
    display: inline-block;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    color: white;
    text-align: center;
    line-height: 24px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 0.5rem;
}

.stage-title {
    font-weight: 600;
    color: var(--text);
    font-size: 0.9rem;
}

.stage-subtitle {
    display: block;
    font-size: 0.75rem;
    color: var(--text-muted);
}

.stage-items {
    list-style: none;
    margin: 0;
    padding: 0;
}

.stage-items li {
    font-size: 0.8rem;
    color: var(--secondary);
    margin-bottom: 0.25rem;
    padding-left: 0.75rem;
    position: relative;
}

.stage-items li::before {
    content: "▪";
    position: absolute;
    left: 0;
    color: var(--primary);
}

.process-arrow {
    display: flex;
    align-items: center;
    font-size: 1.5rem;
    color: var(--primary);
    opacity: 0.5;
}

.process-footer {
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px dashed var(--border);
    font-size: 0.9rem;
    color: var(--text-muted);
    text-align: center;
}

/* Quarterly Roadmap */
.quarterly-roadmap {
    margin: 2rem 0;
    padding: 2rem;
    background: linear-gradient(135deg, #f8fafc 0%, #f0f9ff 100%);
    border-radius: 12px;
    border: 1px solid var(--border);
}

.roadmap-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1.5rem;
    text-align: center;
}

.roadmap-quarters {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
}

.quarter-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.quarter-header {
    padding: 1rem;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.quarter-name {
    font-weight: 700;
    font-size: 1.1rem;
}

.quarter-period {
    font-size: 0.85rem;
    opacity: 0.9;
}

.quarter-items {
    list-style: none;
    margin: 0;
    padding: 1rem;
}

.quarter-items li {
    font-size: 0.85rem;
    color: var(--text);
    margin-bottom: 0.5rem;
    padding-left: 1.25rem;
    position: relative;
}

.quarter-items li::before {
    content: "▪";
    position: absolute;
    left: 0;
    color: var(--primary);
}

.quarter-kpi {
    padding: 0.75rem 1rem;
    background: #f8fafc;
    font-size: 0.85rem;
    color: var(--primary);
    border-top: 1px solid var(--border);
}

/* Brand Positioning */
.brand-positioning {
    margin: 2rem 0;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.positioning-comparison {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.positioning-old, .positioning-new {
    flex: 1;
    min-width: 200px;
    max-width: 280px;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
}

.positioning-old {
    background: #f1f5f9;
    border: 2px solid #e2e8f0;
}

.positioning-new {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border: 2px solid #3b82f6;
}

.positioning-label {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}

.positioning-text {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
}

.positioning-new .positioning-text {
    color: var(--primary);
}

.positioning-arrow {
    font-size: 2rem;
    color: var(--primary);
}

.positioning-reasons {
    background: #f8fafc;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.reasons-title {
    font-weight: 600;
    color: var(--text);
    margin-bottom: 1rem;
}

.positioning-reasons ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.positioning-reasons li {
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.positioning-message {
    padding: 1rem;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border-radius: 8px;
    color: white;
    text-align: center;
    font-size: 1rem;
}

/* Competition Map */
.competition-map {
    margin: 2rem 0;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.map-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1.5rem;
    text-align: center;
}

.map-container {
    display: flex;
    align-items: stretch;
}

.map-axis-y {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-right: 1rem;
    width: 80px;
}

.map-grid {
    flex: 1;
    position: relative;
    height: 300px;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border: 1px solid var(--border);
    border-radius: 8px;
}

.map-axis-x {
    position: absolute;
    bottom: -30px;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
}

.axis-label {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.axis-label.top { margin-bottom: auto; }
.axis-label.bottom { margin-top: auto; }

.map-point {
    position: absolute;
    transform: translate(-50%, -50%);
    text-align: center;
}

.point-marker {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    margin: 0 auto 0.25rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.point-label {
    font-weight: 700;
    font-size: 0.85rem;
}

.point-desc {
    font-size: 0.7rem;
    color: var(--text-muted);
    white-space: nowrap;
}

/* Info Box (Generic) */
.info-box {
    margin: 2rem 0;
    padding: 1.5rem;
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    border-left: 4px solid var(--primary);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-box-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1rem;
}

.info-box-items {
    list-style: none;
    margin: 0;
    padding: 0;
}

.info-box-items li {
    font-size: 0.9rem;
    color: var(--text);
    margin-bottom: 0.5rem;
    padding-left: 1.25rem;
    position: relative;
}

.info-box-items li::before {
    content: "▪";
    position: absolute;
    left: 0;
    color: var(--primary);
}

/* Responsive for new charts */
@media (max-width: 768px) {
    .process-stages {
        flex-direction: column;
    }

    .process-stage {
        max-width: 100%;
    }

    .process-arrow {
        transform: rotate(90deg);
    }

    .positioning-comparison {
        flex-direction: column;
    }

    .positioning-old, .positioning-new {
        max-width: 100%;
    }

    .map-grid {
        height: 250px;
    }

    .roadmap-quarters {
        grid-template-columns: 1fr;
    }
}
'''


def get_scripts() -> str:
    """Return embedded JavaScript."""
    return '''
// Smooth scroll for TOC links
document.querySelectorAll('.toc a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').slice(1);
        const target = document.getElementById(targetId);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Highlight active TOC item on scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            document.querySelectorAll('.toc a').forEach(a => a.classList.remove('active'));
            const id = entry.target.id;
            const tocLink = document.querySelector(`.toc a[href="#${id}"]`);
            if (tocLink) tocLink.classList.add('active');
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('h2, h3').forEach(heading => {
    if (heading.id) observer.observe(heading);
});
'''


def main():
    parser = argparse.ArgumentParser(
        description='Convert Deep Researcher markdown reports to HTML'
    )
    parser.add_argument('input', help='Input markdown file path')
    parser.add_argument('-o', '--output', help='Output HTML file path (optional)')
    parser.add_argument('--title', default='Research Report', help='Document title')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Read markdown content
    md_content = input_path.read_text(encoding='utf-8')

    # Convert to HTML
    html_content = md_to_html(md_content, args.title)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.html')

    # Write HTML
    output_path.write_text(html_content, encoding='utf-8')
    print(f"HTML report generated: {output_path}")

    return str(output_path)


if __name__ == '__main__':
    main()

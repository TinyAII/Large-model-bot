    async def text_to_image_problem_solving_style(self, text: str) -> str:
        """解题助手专用样式"""
        # 将文本内容转换为结构化HTML
        lines = text.split('\n')
        html_parts = []
        current_section = ""
        
        for line in lines:
            line = line.rstrip()
            
            # 检测标题行
            if line.startswith('题目：'):
                current_section = "question"
                html_parts.append('<div class="section-title">题目：</div>')
                continue
            elif line.startswith('思考过程：'):
                current_section = "thinking"
                html_parts.append('<div class="section-title">思考过程：</div>')
                html_parts.append('<div class="thinking-section">')
                continue
            elif line.startswith('答案：'):
                current_section = "answer"
                html_parts.append('<div class="section-title">答案：</div>')
                html_parts.append('<div class="answer-section">')
                continue
            elif line.startswith('时间：'):
                current_section = "time"
                html_parts.append('<div class="section-title">时间：</div>')
                continue
            
            # 处理内容行
            if line.strip():
                html_parts.append(f'<div class="content-line">{line}</div>')
            else:
                # 处理空行，结束当前区块
                if current_section == "thinking":
                    html_parts.append('</div>')
                elif current_section == "answer":
                    html_parts.append('</div>')
                current_section = ""
        
        # 确保所有区块都关闭
        if current_section == "thinking":
            html_parts.append('</div>')
        elif current_section == "answer":
            html_parts.append('</div>')
        
        # 组装最终HTML内容
        formatted_html = '\n'.join(html_parts)
        
        # 使用解题助手专用模板
        problem_solving_template = '''
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>解题助手</title>
            <style>
                body {
                    font-family: 'Microsoft YaHei', Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 20px;
                    line-height: 1.8;
                }
                .container {
                    max-width: 850px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 40px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                }
                .content {
                    white-space: pre-wrap;
                    font-size: 18px;
                    color: #333;
                    text-align: left;
                }
                .section-title {
                    font-size: 22px;
                    font-weight: bold;
                    color: #28a745;
                    margin: 20px 0 10px 0;
                    padding: 8px 0;
                    border-bottom: 2px solid #e8f5e8;
                }
                .content-line {
                    margin: 5px 0;
                }
                .thinking-section {
                    margin-bottom: 30px;
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #17a2b8;
                }
                .answer-section {
                    margin-bottom: 30px;
                    background-color: #fff3cd;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #ffc107;
                }
                .highlight {
                    color: #dc3545;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">{content}</div>
            </div>
        </body>
        </html>
        '''
        
        # 渲染HTML模板
        html_content = problem_solving_template.replace("{content}", formatted_html)
        
        # 使用html_render函数生成图片
        options = {
            "full_page": True,
            "type": "jpeg",
            "quality": 95,
        }
        
        image_url = await self.html_render(
            html_content,
            {},
            True,
            options
        )
        
        return image_url
    
    async def text_to_image_model_menu_style(self, text: str) -> str:
        """大模型菜单专用样式"""
        # 将文本内容转换为结构化HTML
        lines = text.split('\n')
        html_parts = []
        current_section = ""
        
        for line in lines:
            line = line.rstrip()
            
            # 检测是否为大模型菜单
            if line == "大模型菜单":
                # 大模型菜单标题已在模板中处理
                continue
            
            # 检测分类标题
            elif line.startswith('一、') or line.startswith('二、') or line.startswith('三、') or line.startswith('四、'):
                category_name = line.split('、')[1]
                html_parts.append(f'<h2 class="category-title">{category_name}</h2>')
                continue
            
            # 检测模型条目
            elif ' - ' in line:
                # 解析模型条目
                model_part, desc_part = line.split(' - ', 1)
                
                # 检测是否包含示例格式
                if '<提问内容>' in model_part or '<6位数字>' in model_part or '<图片>' in model_part or '<题目内容>' in model_part:
                    # 这是一个模型命令格式
                    model_format = model_part.strip()
                    model_desc = desc_part.strip()
                    
                    # 提取模型名称
                    if ' ' in model_format:
                        model_name = model_format.split(' ')[0]
                    else:
                        model_name = model_format
                    
                    # 生成示例
                    example = model_format.replace('<提问内容>', '1+1').replace('<6位数字>', '123456').replace('<图片>', '[图片]').replace('<题目内容>', '1+1')
                    
                    # 生成HTML
                    html_parts.append(f'<div class="model-item">')
                    html_parts.append(f'<span class="model-name">{model_name}</span> ')
                    html_parts.append(f'<span class="model-format">{model_format}</span> ')
                    html_parts.append(f'<span class="separator">---------------</span> ')
                    html_parts.append(f'<span class="example">示例：{example}（注意有空格）</span> ')
                    html_parts.append(f'<span class="separator">----------</span> ')
                    html_parts.append(f'<span class="model-desc">{model_desc}</span>')
                    html_parts.append(f'</div>')
            
            # 处理空行
            elif line.strip() == '':
                continue
            
            # 处理其他文本行
            else:
                html_parts.append(f'<div class="content-line">{line}</div>')
        
        # 组装最终HTML内容
        formatted_html = '\n'.join(html_parts)
        
        # 使用大模型菜单专用模板
        model_menu_template = '''
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>大模型菜单</title>
            <style>
                body {
                    font-family: 'Microsoft YaHei', Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 20px;
                    line-height: 2.0;
                }
                .container {
                    max-width: 950px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 40px;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                }
                .menu-title {
                    font-size: 32px;
                    font-weight: bold;
                    color: #28a745;
                    text-align: center;
                    margin-bottom: 40px;
                    padding: 15px;
                    background-color: #e8f5e8;
                    border-radius: 8px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                }
                .category-title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #17a2b8;
                    margin: 30px 0 20px 0;
                    padding: 10px 0;
                    border-bottom: 3px solid #17a2b8;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                .model-item {
                    font-size: 18px;
                    line-height: 2.2;
                    margin: 15px 0;
                    padding: 10px;
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    border-left: 4px solid #ffc107;
                }
                .model-name {
                    font-weight: bold;
                    color: #dc3545;
                    font-size: 20px;
                }
                .model-format {
                    color: #333;
                    font-weight: normal;
                }
                .example {
                    color: #6c757d;
                    margin: 0 10px;
                }
                .model-desc {
                    color: #495057;
                    font-weight: bold;
                }
                .separator {
                    color: #adb5bd;
                    margin: 0 10px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="menu-title">大模型菜单</h1>
                {content}
            </div>
        </body>
        </html>
        '''
        
        # 渲染HTML模板
        html_content = model_menu_template.replace("{content}", formatted_html)
        
        # 使用html_render函数生成图片
        options = {
            "full_page": True,
            "type": "jpeg",
            "quality": 95,
        }
        
        image_url = await self.html_render(
            html_content,
            {},
            True,
            options
        )
        
        return image_url
    
    async def text_to_image_default_style(self, text: str) -> str:
        """默认样式"""
        # 使用原始模板
        html_content = self.MENU_TEMPLATE.replace("{{content}}", text)
        
        # 使用html_render函数生成图片
        options = {
            "full_page": True,
            "type": "jpeg",
            "quality": 95,
        }
        
        image_url = await self.html_render(
            html_content,
            {},
            True,
            options
        )
        
        return image_url
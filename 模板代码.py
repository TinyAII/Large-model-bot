# 首先定义HTML模板
INFO_LIST_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            padding: 30px;
            background: #ffffff;
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
        
        .container {
            position: relative;
            width: 500px;  /* 调整宽度 */
            margin: 0 auto;
        }
        
        .grid-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            min-height: 100%;
            background-image: 
                linear-gradient(to right, #e0e0e0 1px, transparent 1px),
                linear-gradient(to bottom, #e0e0e0 1px, transparent 1px);
            background-size: 25px 25px;
            opacity: 0.2;
            z-index: 0;
        }
        
        .main-border {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            min-height: 100%;
            border: 2px solid #000000;
            z-index: 1;
        }
        
        .corner {
            position: absolute;
            width: 16px;
            height: 16px;
            border: 2px solid #000000;
            z-index: 2;
        }
        
        .corner-tl {
            top: -8px;
            left: -8px;
            border-right: none;
            border-bottom: none;
        }
        
        .corner-tr {
            top: -8px;
            right: -8px;
            border-left: none;
            border-bottom: none;
        }
        
        .corner-bl {
            bottom: -8px;
            left: -8px;
            border-right: none;
            border-top: none;
        }
        
        .corner-br {
            bottom: -8px;
            right: -8px;
            border-left: none;
            border-top: none;
        }
        
        .info-list {
            position: relative;
            z-index: 3;
            padding: 40px 30px;
        }
        
        .info-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 30px;
            padding-bottom: 25px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .info-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .item-number {
            width: 30px;
            height: 30px;
            background: #000000;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: bold;
            margin-right: 20px;
            flex-shrink: 0;
        }
        
        .item-content {
            flex-grow: 1;
        }
        
        .item-title {
            font-size: 18px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        
        .item-description {
            font-size: 14px;
            color: #666666;
            line-height: 1.6;
        }
        
        .item-meta {
            margin-top: 12px;
            font-size: 12px;
            color: #999999;
            display: flex;
            align-items: center;
        }
        
        .meta-dot {
            display: inline-block;
            width: 4px;
            height: 4px;
            background: #000000;
            border-radius: 50%;
            margin: 0 10px;
        }
        
        .item-divider {
            position: relative;
            height: 1px;
            margin: 15px 0;
            overflow: hidden;
        }
        
        .item-divider::after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                to right,
                transparent,
                transparent 5px,
                #e0e0e0 5px,
                #e0e0e0 10px
            );
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="grid-background"></div>
        <div class="main-border"></div>
        <div class="corner corner-tl"></div>
        <div class="corner corner-tr"></div>
        <div class="corner corner-bl"></div>
        <div class="corner corner-br"></div>
        
        <div class="info-list">
            {% for item in items %}
            <div class="info-item">
                <div class="item-number">{{ loop.index }}</div>
                <div class="item-content">
                    <div class="item-title">{{ item.title }}</div>
                    <div class="item-description">{{ item.description }}</div>
                    
                    {% if item.time or item.category %}
                    <div class="item-meta">
                        {% if item.time %}<span>{{ item.time }}</span>{% endif %}
                        {% if item.time and item.category %}<span class="meta-dot"></span>{% endif %}
                        {% if item.category %}<span>{{ item.category }}</span>{% endif %}
                    </div>
                    {% endif %}
                </div>
            </div>
            
            {% if not loop.last %}
            <div class="item-divider"></div>
            {% endif %}
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

# Python使用代码
@filter.command("infolist")
async def infolist_command(self, event: AstrMessageEvent, *args):
    """
    使用方式：
    /infolist 显示默认信息列表
    /infolist 标题1|描述1|时间1|分类1 标题2|描述2|时间2|分类2 ...
    
    参数说明：用竖线分隔，格式为：标题|描述|时间|分类
    其中时间和分类是可选的
    """
    import re
    from datetime import datetime
    
    # 如果没有参数，使用默认数据
    if not args:
        # 默认示例数据
        items = [
            {
                "title": "项目启动会议",
                "description": "讨论新项目需求和技术选型，确定开发时间线",
                "time": "2024-01-15 14:30",
                "category": "会议"
            },
            {
                "title": "完成用户认证模块",
                "description": "实现了OAuth2.0授权流程和JWT令牌验证",
                "time": "2024-01-16 完成",
                "category": "开发"
            },
            {
                "title": "性能优化",
                "description": "优化数据库查询，减少响应时间约40%",
                "time": "2024-01-17",
                "category": "优化"
            },
            {
                "title": "技术分享会",
                "description": "介绍新的微服务架构设计模式",
                "time": "2024-01-18 16:00",
                "category": "分享"
            },
            {
                "title": "代码审查",
                "description": "审查PR #245，重点检查安全性和代码规范",
                "time": "待办",
                "category": "审查"
            }
        ]
    else:
        # 解析用户输入
        items = []
        for arg in args:
            parts = arg.split('|')
            if len(parts) >= 2:
                item = {
                    "title": parts[0].strip(),
                    "description": parts[1].strip()
                }
                if len(parts) > 2:
                    item["time"] = parts[2].strip()
                if len(parts) > 3:
                    item["category"] = parts[3].strip()
                items.append(item)
    
    # 如果没有解析到有效数据，返回提示
    if not items:
        yield event.reply("请输入有效格式：标题|描述 或 标题|描述|时间|分类")
        return
    
    # 截图选项
    options = {
        "full_page": True,  # 让高度自适应内容
        "type": "png",
        "quality": 95,
        "omit_background": False,
        "animations": "disabled",
        "caret": "hide"
    }
    
    try:
        url = await self.html_render(INFO_LIST_TEMPLATE, {"items": items}, options=options)
        yield event.image_result(url)
    except Exception as e:
        yield event.reply(f"生成图片失败: {str(e)}")

# 如果想让命令更简单，可以单独注册一个命令来添加单条信息
@filter.command("addinfo")
async def addinfo_command(self, event: AstrMessageEvent, info_str: str):
    """
    添加单条信息到列表
    格式：/addinfo 标题|描述|时间|分类
    """
    from datetime import datetime
    
    # 这里可以添加逻辑来保存和加载用户的信息列表
    # 例如使用数据库或文件存储
    
    # 暂时返回示例
    items = [
        {
            "title": "你添加的信息",
            "description": info_str.split('|')[1] if '|' in info_str else info_str,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": "用户添加"
        }
    ]
    
    options = {
        "full_page": True,
        "type": "png",
        "quality": 95
    }
    
    url = await self.html_render(INFO_LIST_TEMPLATE, {"items": items}, options=options)
    yield event.image_result(url)
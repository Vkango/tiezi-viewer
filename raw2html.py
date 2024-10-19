import json
from datetime import datetime
html_head = """
<!DOCTYPE html>
<html lang="zh_CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{$title$} - 贴子查看器</title>
    <link rel="stylesheet" type="text/css" href="res/style.css">
</head>
<body>
    <div class="navi">
        <div class="navi-title">
        {$title$}
        </div>
    </div>
    <div class="ba-show" style="border-radius: 20px; background-color: rgba(0,0,0,0.05);width: fit-content; padding-left: 6px; padding-right: 20px; margin-left: 20px; margin-right: 20px;margin-top: 5px; margin-bottom: 10px;">
        <img class="avatar" src="{$bar_avatar$}">
        <span style="font-weight: normal;font-size: 90%;left: 5px; top: -10px;position: relative;">{$bar_name$}</span>
    </div>
    <p style="font-weight: 700; margin-left: 20px; margin-right: 10px">共{$reply_num$}条回复 | 页面{$current_page$}/{$total_page$}</p>

"""
html_content = """
    <div class="content" style="padding-left: 20px;padding-right: 20px;">
        <img class="avatar" src="{$avatar$}">
        <div class="nick">{$nick$}</div>
        <div class="{$level_id$}">{$level$}</div>
        <div class="owner">楼主</div>
        <div class="content">
"""
html_content_content_end = """
        </div>
        <div class="post-info">
            {$floor$}楼 | {$post_time$}
        </div>
"""
html_subpost_begin = """
        <div class="sub-post" style="line-height: 30px;">
"""
html_subpost_end = """
        </div>
"""
html_content_end = """
    </div>"""
html_end = """
    <div class="page-driver">
        <button>上一页</button>
        <button>下一页</button>
        <button>跳页</button>
    </div>
</body>
</html>"""
def read_file(path):
    with open(path, "r", encoding='utf-8') as w:
        # 读取文件的所有行
        lines = w.readlines()
        t = ""
        for i in lines:
            t += i
        return(t)
def convert(string):
    j = json.loads(string)
    output = ""
    # 处理头部
    output += html_head
    output = output.replace("{$title$}", j['thread']['title'])
    output = output.replace("{$bar_name$}", j['forum']['name'])
    output = output.replace("{$bar_avatar$}", j['forum']['avatar'])
    output = output.replace("{$reply_num$}", str(j['page']['total_num']))
    output = output.replace("{$current_page$}", str(j['page']['current_page']))
    output = output.replace("{$total_page$}", str(j['page']['total_page']))
    # 处理内容
    for i in range(len(j['post_list'])):
        # 内容头部
        content = html_content.replace("{$nick$}", j['post_list'][i]['author']['name_show'] + f" ({j['post_list'][i]['author']['name']})")
        content = content.replace("{$level$}", str(j['post_list'][i]['author']['level_id']))
        #content = html_content.replace("{$avatar$}", "src/" + j['post_list'][i]['author']['name'])
        
        content = content.replace("{$avatar$}", "https://himg.bdimg.com/sys/portrait/item/" + j['post_list'][i]['author']['portrait'])
        levelid = j['post_list'][i]['author']['level_id']
        if levelid < 4:
            content = content.replace("{$level_id$}", "level1")
        if levelid >= 4 and levelid < 10:
            content = content.replace("{$level_id$}", "level2")
        if levelid >=10 and levelid < 16:
            content = content.replace("{$level_id$}", "level3")
        if levelid >= 16:
            content = content.replace("{$level_id$}", "level4")
        if not j['thread']['author']['name'] == j['post_list'][i]['author']['name']:
            content = content.replace("""        <div class="owner">楼主</div>""", "")
        
        # 内容正文
        for c in range(len(j['post_list'][i]['content'])):
            if j['post_list'][i]['content'][c]['type'] == 0:
                content += "            " + j['post_list'][i]['content'][c]['text'] +"""
                """
            if j['post_list'][i]['content'][c]['type'] == 4:
                content += "            <a href="">" + j['post_list'][i]['content'][c]['text'] + "</a>" + """
                """
            if j['post_list'][i]['content'][c]['type'] == 2:
                content += f"""            <img src="res/emotion/{j['post_list'][i]['content'][c]['text'] + ".png"}">""" + """
                """
            if j['post_list'][i]['content'][c]['type'] == 3:
                content += f"""            <br><img src="{j['post_list'][i]['content'][c]['src']}"><br>"""  + """
                """
            if j['post_list'][i]['content'][c]['type'] == 1:
                content += f"""            <a href="{j['post_list'][i]['content'][c]['link']}">{j['post_list'][i]['content'][c]['text']}</a>"""  + """
                """
        # 内容尾部
        content += html_content_content_end.replace("{$floor$}", str(j['post_list'][i]['floor']))
        date_obj = datetime.fromtimestamp(j['post_list'][i]['time'])
        content = content.replace("{$post_time$}", date_obj.strftime('%Y-%m-%d %H:%M:%S'))
        
        # 楼中楼
        
        # 结尾
        content += html_content_end
        output += content
    
    # html尾部
    output += html_end
    with open("t.html", "w", encoding="utf-8") as w:
        w.writelines(output)
        w.close()
    return output
        
            
        
        
        
    
    
    
    
convert(read_file("sample.json").replace("\\n", "<br>"))
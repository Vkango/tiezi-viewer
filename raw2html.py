import json,shutil
from datetime import datetime
dir_path = ""
html_head = """
<!DOCTYPE html>
<html lang="zh_CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{$title$} - 贴子查看器</title>
    <link rel="stylesheet" type="text/css" href="res/style.css">
    <script src="res/scripts.js"></script>
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
html_subpost_content = """
            <img class="avatar1" src="{$avatar$}">
            <div class="nick1">{$nick$}</div>
            <div class="s{$level_id$}">{$level$}</div>
            <div class="owner1">楼主</div>
            <small>{$post_time$}</small>
            <br>
            <div class="content">
"""
html_subpost_content_end = """
            </div>"""
html_subpost_end = """
        </div>
"""
html_content_end = """
    </div>"""
html_end = """
    <div class="page-driver">
        <a href={$last_page$}.html>上一页</a>
        <a href={$next_page$}.html>下一页</a>
    </div>
    
        <div id="modal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
          <iframe id="reply-box" src="" frameborder="0"></iframe>

        </div>
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
def write_file(path, data):
    with open(path, "w", encoding="utf-8") as w:
        w.writelines(data)
        w.close()
def convert(string):
    j = json.loads(string)
    output = ""
    # 处理头部
    output += html_head
    output = output.replace("{$title$}", j['thread']['title'])
    output = output.replace("{$bar_name$}", j['forum']['name'])
    output = output.replace("{$bar_avatar$}", j['forum']['avatar'])
    output = output.replace("{$reply_num$}", str(j['thread']['reply_num']))
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
                content += f"""            <br><img src="res/{j['post_list'][i]['content'][c]['src'][-44:]}"><br>"""  + """
                """
            if j['post_list'][i]['content'][c]['type'] == 1:
                content += f"""            <a href="{j['post_list'][i]['content'][c]['link']}">{j['post_list'][i]['content'][c]['text']}</a>"""  + """
                """
        # 内容尾部
        content += html_content_content_end.replace("{$floor$}", str(j['post_list'][i]['floor']))
        date_obj = datetime.fromtimestamp(j['post_list'][i]['time'])
        content = content.replace("{$post_time$}", date_obj.strftime('%Y-%m-%d %H:%M:%S'))
        # 结尾
        content += html_content_end
        
        if j['post_list'][i]['sub_post_number'] > 0:
            page1 = json.loads(read_file(dir_path + "\\res\\" + str(j['post_list'][i]['id']) + "\\0.json"))
            content += html_subpost_begin
            cycle_ = 3
            print(j['post_list'][i]['sub_post_number'],j['post_list'][i]['sub_post_number'],dir_path + "\\res\\" + str(j['post_list'][i]['id']) + "\\0.json")
            if len(page1['subpost_list']) <= 3:
                # cycle_ = j['post_list'][i]['sub_post_number'] 此写法理应正确，但是会爆出outrange，所以只能强制使用len
                cycle_ = len(page1['subpost_list'])
            for m in range(cycle_):
                content += html_subpost_content
                date_obj = datetime.fromtimestamp(page1['subpost_list'][m]['time'])
                content = content.replace("{$post_time$}", date_obj.strftime('%Y-%m-%d %H:%M:%S'))
                content = content.replace("{$nick$}", page1['subpost_list'][m]['author']['name_show'] + f" ({page1['subpost_list'][m]['author']['name']})")
                content = content.replace("{$level$}", str(page1['subpost_list'][m]['author']['level_id']))
                #content = html_content.replace("{$avatar$}", "src/" + j['post_list'][i]['author']['name'])
                
                content = content.replace("{$avatar$}", "https://himg.bdimg.com/sys/portrait/item/" + page1['subpost_list'][m]['author']['portrait'])
                levelid = page1['subpost_list'][m]['author']['level_id']
                if levelid < 4:
                    content = content.replace("{$level_id$}", "level1")
                if levelid >= 4 and levelid < 10:
                    content = content.replace("{$level_id$}", "level2")
                if levelid >=10 and levelid < 16:
                    content = content.replace("{$level_id$}", "level3")
                if levelid >= 16:
                    content = content.replace("{$level_id$}", "level4")
                if not j['thread']['author']['name'] == page1['subpost_list'][m]['author']['name']:
                    content = content.replace("""        <div class="owner1">楼主</div>""", "")
                
                # 内容正文
                for c in range(len(page1['subpost_list'][m]['content'])):
                    if page1['subpost_list'][m]['content'][c]['type'] == 0:
                        content += "            " + page1['subpost_list'][m]['content'][c]['text'] +"""
                        """
                    if page1['subpost_list'][m]['content'][c]['type'] == 4:
                        content += "            <a href="">" + page1['subpost_list'][m]['content'][c]['text'] + "</a>" + """
                        """
                    if page1['subpost_list'][m]['content'][c]['type'] == 2:
                        content += f"""            <img src="res/emotion/{page1['subpost_list'][m]['content'][c]['text'] + ".png"}">""" + """
                        """
                    if page1['subpost_list'][m]['content'][c]['type'] == 3:
                        content += f"""            <br><img src="res/{page1['subpost_list'][m]['content'][c]['src'][-44:]}"><br>"""  + """
                        """
                    if page1['subpost_list'][m]['content'][c]['type'] == 1:
                        content += f"""            <a href="{page1['subpost_list'][m]['content'][c]['link']}">{page1['subpost_list'][m]['content'][c]['text']}</a>"""  + """
                        """
                content += html_subpost_content_end
            if j['post_list'][i]['sub_post_number'] > 3:
                content += f"""
                <button style="margin-top: 10px; margin-bottom: 10px" onclick="btnclick('{str(j['post_list'][i]['id'])}')">查看 {str(j['post_list'][i]['sub_post_number'])} 条回复</button>
                """            
            content += html_subpost_end
            
            # 处理全部楼中楼并输出。此处内容不应保存至HTML文件。
            subpost_output = """<!DOCTYPE html>
<head>
    <link rel="stylesheet" href="style.css">
</head>
<body>"""
            for q in range(page1['page']['total_page']):
                Subpage = json.loads(read_file(dir_path + "\\res\\" + str(j['post_list'][i]['id']) + f"\\{str(q)}.json"))
                for m in range(len(Subpage['subpost_list'])):
                    subpost_output += html_subpost_content
                    date_obj = datetime.fromtimestamp(Subpage['subpost_list'][m]['time'])
                    subpost_output = subpost_output.replace("{$post_time$}", date_obj.strftime('%Y-%m-%d %H:%M:%S'))
                    subpost_output = subpost_output.replace("{$nick$}", Subpage['subpost_list'][m]['author']['name_show'] + f" ({Subpage['subpost_list'][m]['author']['name']})")
                    subpost_output = subpost_output.replace("{$level$}", str(Subpage['subpost_list'][m]['author']['level_id']))
                    #content = html_content.replace("{$avatar$}", "src/" + j['post_list'][i]['author']['name'])
                    
                    subpost_output = subpost_output.replace("{$avatar$}", "https://himg.bdimg.com/sys/portrait/item/" + Subpage['subpost_list'][m]['author']['portrait'])
                    levelid = page1['subpost_list'][m]['author']['level_id']
                    if levelid < 4:
                        subpost_output = subpost_output.replace("{$level_id$}", "level1")
                    if levelid >= 4 and levelid < 10:
                        subpost_output = subpost_output.replace("{$level_id$}", "level2")
                    if levelid >=10 and levelid < 16:
                        subpost_output = subpost_output.replace("{$level_id$}", "level3")
                    if levelid >= 16:
                        subpost_output = subpost_output.replace("{$level_id$}", "level4")
                    if not j['thread']['author']['name'] == Subpage['subpost_list'][m]['author']['name']:
                        subpost_output = subpost_output.replace("""        <div class="owner1">楼主</div>""", "")
                    
                    # 内容正文
                    for c in range(len(Subpage['subpost_list'][m]['content'])):
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 0:
                            subpost_output += "            " + Subpage['subpost_list'][m]['content'][c]['text'] +"""
                            """
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 4:
                            subpost_output += "            <a href="">" + Subpage['subpost_list'][m]['content'][c]['text'] + "</a>" + """
                            """
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 2:
                            subpost_output += f"""            <img src="emotion/{Subpage['subpost_list'][m]['content'][c]['text'] + ".png"}">""" + """
                            """
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 3:
                            subpost_output += f"""            <br><img src="{(Subpage['subpost_list'][m]['content'][c]['src'])[-44:]}"><br>"""  + """
                            """
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 1:
                            subpost_output += f"""            <a href="{Subpage['subpost_list'][m]['content'][c]['link']}">{Subpage['subpost_list'][m]['content'][c]['text']}</a>"""  + """
                            """
                    subpost_output += html_subpost_end
                    subpost_output += html_subpost_content_end
            write_file(dir_path + "\\res\\" + str(j['post_list'][i]['id']) + ".html", subpost_output)
        
        # 别急我们又回来了
        output += content
    # html尾部
    output += html_end
    if j['page']['current_page'] == 1:
        output = output.replace("""<a href={$last_page$}.html>上一页</a>""","")
    if j['page']['current_page'] == j['page']['total_page']:
        output = output.replace("""<a href={$next_page$}.html>下一页</a>""","")
    output = output.replace("{$last_page$}", str(j['page']['current_page'] - 1))
    output = output.replace("{$next_page$}", str(j['page']['current_page'] + 1))
    return output
print("请输入贴子tid文件夹所在目录（含tid号）：")

dir_path = input() + "\\"
d = json.loads(read_file(dir_path + "1.json"))
for i in range(d['page']['total_page']):
    print("converting page: ", i + 1)
    write_file(dir_path + str(i + 1) + ".html", convert(read_file(dir_path + str(i + 1) + ".json").replace("\\n", "<br>")))
print("copying rescouces...")
try:
    shutil.copytree(".\\res\\emotion", dir_path + "\\res\\emotion")
except:
    None
try:
    shutil.copy("scripts.js", dir_path + "\\res\\scripts.js")
except:
    None
try:
    shutil.copy("style.css", dir_path + "\\res\\style.css")
except:
    None
=======
import json,shutil
from datetime import datetime
dir_path = ""
html_head = """
<!DOCTYPE html>
<html lang="zh_CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{$title$} - 贴子查看器</title>
    <link rel="stylesheet" type="text/css" href="res/style.css">
    <script src="res/scripts.js"></script>
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
html_subpost_content = """
            <img class="avatar1" src="{$avatar$}">
            <div class="nick1">{$nick$}</div>
            <div class="s{$level_id$}">{$level$}</div>
            <div class="owner1">楼主</div>
            {$post_time$}
            <br>
            <div class="content">
"""
html_subpost_content_end = """
            </div>"""
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
    
        <div id="modal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
          <iframe id="reply-box" src="109754979677.html" frameborder="0"></iframe>

        </div>
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
def write_file(path, data):
    with open(path, "w", encoding="utf-8") as w:
        w.writelines(data)
        w.close()
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
                content += f"""            <br><img src="res/{j['post_list'][i]['content'][c]['src'][-44:]}"><br>"""  + """
                """
            if j['post_list'][i]['content'][c]['type'] == 1:
                content += f"""            <a href="{j['post_list'][i]['content'][c]['link']}">{j['post_list'][i]['content'][c]['text']}</a>"""  + """
                """
        # 内容尾部
        content += html_content_content_end.replace("{$floor$}", str(j['post_list'][i]['floor']))
        date_obj = datetime.fromtimestamp(j['post_list'][i]['time'])
        content = content.replace("{$post_time$}", date_obj.strftime('%Y-%m-%d %H:%M:%S'))
        # 结尾
        content += html_content_end
        
        if j['post_list'][i]['sub_post_number'] > 0:
            page1 = json.loads(read_file(dir_path + "\\res\\" + str(j['post_list'][i]['id']) + "\\0.json"))
            content += html_subpost_begin
            cycle_ = 3
            if j['post_list'][i]['sub_post_number'] <= 3:
                cycle_ = j['post_list'][i]['sub_post_number']
            for m in range(cycle_):
                content += html_subpost_content
                date_obj = datetime.fromtimestamp(page1['subpost_list'][m]['time'])
                content = content.replace("{$post_time$}", date_obj.strftime('%Y-%m-%d %H:%M:%S'))
                content = content.replace("{$nick$}", page1['subpost_list'][m]['author']['name_show'] + f" ({page1['subpost_list'][m]['author']['name']})")
                content = content.replace("{$level$}", str(page1['subpost_list'][m]['author']['level_id']))
                #content = html_content.replace("{$avatar$}", "src/" + j['post_list'][i]['author']['name'])
                
                content = content.replace("{$avatar$}", "https://himg.bdimg.com/sys/portrait/item/" + page1['subpost_list'][m]['author']['portrait'])
                levelid = page1['subpost_list'][m]['author']['level_id']
                if levelid < 4:
                    content = content.replace("{$level_id$}", "level1")
                if levelid >= 4 and levelid < 10:
                    content = content.replace("{$level_id$}", "level2")
                if levelid >=10 and levelid < 16:
                    content = content.replace("{$level_id$}", "level3")
                if levelid >= 16:
                    content = content.replace("{$level_id$}", "level4")
                if not j['thread']['author']['name'] == page1['subpost_list'][m]['author']['name']:
                    content = content.replace("""        <div class="owner1">楼主</div>""", "")
                
                # 内容正文
                for c in range(len(page1['subpost_list'][m]['content'])):
                    if page1['subpost_list'][m]['content'][c]['type'] == 0:
                        content += "            " + page1['subpost_list'][m]['content'][c]['text'] +"""
                        """
                    if page1['subpost_list'][m]['content'][c]['type'] == 4:
                        content += "            <a href="">" + page1['subpost_list'][m]['content'][c]['text'] + "</a>" + """
                        """
                    if page1['subpost_list'][m]['content'][c]['type'] == 2:
                        content += f"""            <img src="res/emotion/{page1['subpost_list'][m]['content'][c]['text'] + ".png"}">""" + """
                        """
                    if page1['subpost_list'][m]['content'][c]['type'] == 3:
                        content += f"""            <br><img src="res/{page1['subpost_list'][m]['content'][c]['src'][-44:]}"><br>"""  + """
                        """
                    if page1['subpost_list'][m]['content'][c]['type'] == 1:
                        content += f"""            <a href="{page1['subpost_list'][m]['content'][c]['link']}">{page1['subpost_list'][m]['content'][c]['text']}</a>"""  + """
                        """
                content += html_subpost_content_end
            if j['post_list'][i]['sub_post_number'] > 3:
                content += f"""
                <button style="margin-top: 10px; margin-bottom: 10px" onclick="btnclick('{str(j['post_list'][i]['id'])}')">查看 {str(j['post_list'][i]['sub_post_number'])} 条回复</button>
                """            
            content += html_subpost_end
            
            # 处理全部楼中楼并输出。此处内容不应保存至HTML文件。
            subpost_output = """<!DOCTYPE html>
<head>
    <link rel="stylesheet" href="style.css">
</head>
<body>"""
            for q in range(page1['page']['total_page']):
                Subpage = json.loads(read_file(dir_path + "\\res\\" + str(j['post_list'][i]['id']) + f"\\{str(q)}.json"))
                for m in range(len(Subpage['subpost_list'])):
                    subpost_output += html_subpost_content
                    date_obj = datetime.fromtimestamp(Subpage['subpost_list'][m]['time'])
                    subpost_output = subpost_output.replace("{$post_time$}", date_obj.strftime('%Y-%m-%d %H:%M:%S'))
                    subpost_output = subpost_output.replace("{$nick$}", Subpage['subpost_list'][m]['author']['name_show'] + f" ({Subpage['subpost_list'][m]['author']['name']})")
                    subpost_output = subpost_output.replace("{$level$}", str(Subpage['subpost_list'][m]['author']['level_id']))
                    #content = html_content.replace("{$avatar$}", "src/" + j['post_list'][i]['author']['name'])
                    
                    subpost_output = subpost_output.replace("{$avatar$}", "https://himg.bdimg.com/sys/portrait/item/" + Subpage['subpost_list'][m]['author']['portrait'])
                    levelid = page1['subpost_list'][m]['author']['level_id']
                    if levelid < 4:
                        subpost_output = subpost_output.replace("{$level_id$}", "level1")
                    if levelid >= 4 and levelid < 10:
                        subpost_output = subpost_output.replace("{$level_id$}", "level2")
                    if levelid >=10 and levelid < 16:
                        subpost_output = subpost_output.replace("{$level_id$}", "level3")
                    if levelid >= 16:
                        subpost_output = subpost_output.replace("{$level_id$}", "level4")
                    if not j['thread']['author']['name'] == Subpage['subpost_list'][m]['author']['name']:
                        subpost_output = subpost_output.replace("""        <div class="owner1">楼主</div>""", "")
                    
                    # 内容正文
                    for c in range(len(Subpage['subpost_list'][m]['content'])):
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 0:
                            subpost_output += "            " + Subpage['subpost_list'][m]['content'][c]['text'] +"""
                            """
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 4:
                            subpost_output += "            <a href="">" + Subpage['subpost_list'][m]['content'][c]['text'] + "</a>" + """
                            """
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 2:
                            subpost_output += f"""            <img src="emotion/{Subpage['subpost_list'][m]['content'][c]['text'] + ".png"}">""" + """
                            """
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 3:
                            subpost_output += f"""            <br><img src="{(Subpage['subpost_list'][m]['content'][c]['src'])[-44:]}"><br>"""  + """
                            """
                        if Subpage['subpost_list'][m]['content'][c]['type'] == 1:
                            subpost_output += f"""            <a href="{Subpage['subpost_list'][m]['content'][c]['link']}">{Subpage['subpost_list'][m]['content'][c]['text']}</a>"""  + """
                            """
                    subpost_output += html_subpost_end
                    subpost_output += html_subpost_content_end
            write_file(dir_path + "\\res\\" + str(j['post_list'][i]['id']) + ".html", subpost_output)
        
        # 别急我们又回来了
        output += content
    # html尾部
    output += html_end
    return output
print("请输入贴子tid文件夹所在目录（含tid号）：")

dir_path = input() + "\\"
d = json.loads(read_file(dir_path + "1.json"))
for i in range(d['page']['total_page']):
    print("converting page: ", i + 1)
    write_file(dir_path + str(i + 1) + ".html", convert(read_file(dir_path + str(i + 1) + ".json").replace("\\n", "<br>")))
print("copying rescouces...")
try:
    shutil.copytree(".\\res\\emotion", dir_path + "\\res\\emotion")
except:
    None
try:
    shutil.copy("scripts.js", dir_path + "\\res\\scripts.js")
except:
    None
try:
    shutil.copy("style.css", dir_path + "\\res\\style.css")
except:
    None
>>>>>>> 9442ecc11525dda47ea4eb4b292f8bbd7e7b88ec
print("task finished.")
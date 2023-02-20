import json,os,shutil

from doodstream import DoodStream

d = DoodStream('My Api Key')
start_folder_id=""
page=0
f_id=""
base_folder_fanart='https://www.beermoneyforum.com/blog/wp-content/uploads/2020/04/doodstream-logo.png'
base_folder_icon='https://pbs.twimg.com/profile_images/1590730546392408065/nRBKYofN_400x400.jpg'
base_server_folder="https://www.myserver.com/"
if os.path.exists('output'):
    shutil.rmtree('output')
if not os.path.exists('output'):
     os.makedirs('output')
import re
def alphaNumOrder(string):
   """ Returns all numbers on 5 digits to let sort the string with numeric order.
   Ex: alphaNumOrder("a6b12.125")  ==> "a00006b00012.00125"
   """
   return ''.join([format(int(x), '05d') if x.isdigit()
                   else x for x in re.split(r'(\d+)', string['title'])])


def make_folder_file(f_id,next_path_pre,output_name):
    
    json_file={}
    json_file['items']=[]
    all_results=d.list_folders(page,f_id)

    if 'folders' in all_results['result']:
     for items in all_results['result']['folders']:
        json_item={}
        
        json_item['fanart']=base_folder_fanart
        json_item['thumbnail']=base_folder_icon
        json_item['summary']=" "
        json_item['title']=items['name']
        json_item['folder_id']=items['fld_id']
        
        
        json_item['link']=base_server_folder+'/'+next_path_pre.replace('\\','/')+'/'+items['name'].replace(" ","_")+'/'+items['name'].replace(" ","_")+'.json'
        json_item['type']='dir'
        json_item['content']=" "
        json_file['items'].append(json_item)
        
        next_path=os.path.join(next_path_pre,items['name'].replace(" ","_"))
        if not os.path.exists(next_path):
            os.makedirs(next_path)
        print(next_path)
        make_folder_file(items['fld_id'],next_path,items['name'].replace(" ","_"))
        
        
    if 'files' in all_results['result']:
     for items in all_results['result']['files']:

        iconimage=items['single_img']
        fanart=iconimage
        description=items['title']
        json_item={}
        
        json_item['fanart']=fanart
        json_item['thumbnail']=iconimage
        json_item['summary']=" "
        json_item['title']=items['title']
        json_item['link']=items['download_url']
        json_item['type']='item'
        json_item['content']=" "
        json_file['items'].append(json_item)
    
    
    json_file['items'].sort(key=alphaNumOrder)
    #json_file['items'].sort(key=lambda x: x["title"])
    out_file = open(os.path.join(next_path_pre,output_name+".json"), "w")
    
    json.dump(json_file,out_file, indent = 6)
make_folder_file(start_folder_id,"output","main.json")
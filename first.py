import pprint
from threadgenius import ThreadGenius
from threadgenius.types import ImageFileInput, ImageUrlInput
from glob import glob
from tkinter import *
from PIL import Image, ImageTk
from gui import GUI

root = Tk()
root.configure(background='black')
my_gui = GUI(root, '/Users/aiwabdn/Downloads/views')
root.mainloop()
root.destroy()


img_ids = [1112271, 1112822, 1313147, 1321373, 1985246, 2255126, 2805346, 6899913, 7921937, 9191860, 10268661, 10309827, 10504174, 11243566, 11265539, 11354115, 11392078, 11686056, 11950037, 11950733, 12158645, 12221846, 12818421, 13051183, 13057723, 13065171, 13066776, 13080489, 13081006, 13104571]

for i in img_ids:
    print i
    try:
        image = ImageFileInput(file_object=open(img_path+str(i)+'.jpg', 'rb'))
        resp = tg.tag_image(image)
        img_url = resp['response']['prediction']['image']['url']
        tags[i] = [(_['type'], _['name'], _['confidence']) for _ in resp['response']['prediction']['data']['tags'] if _['confidence']>threshold]
        image = ImageUrlInput(img_url)
        resp = tg.detect_image(image)
        boxes[i] = [(_['category'], _['score'], _['bbox']) for _ in resp['response']['prediction']['data']['detections'] if _['score']>threshold]
        image = ImageUrlInput(img_url)
        resp = tg.search_by_image(
                catalog_gid='shopstyle',
                image=image,
                n_results=5)
        catalog_ss[i] = [(_['object']['metadata'], _['score']) for _ in resp['response']['results'] if _['score']>threshold]
        image = ImageUrlInput(img_url)
        resp = tg.search_by_image(
                catalog_gid='bloglovin_fashion',
                image=image,
                n_results=5)
        catalog_bl[i] = [(_['object']['metadata'], _['score']) for _ in resp['response']['results'] if _['score']>threshold]
    except:
        continue
    print '+++++++++++++'

        #Button(self.root, text='detect items', command=self.get_tags).grid(row=2, column=1)
        #Button(self.root, text='ShopStyle', command=self.get_tags).grid(row=3, column=1)
        #Button(self.root, text="Blog Lovin'", command=self.get_tags).grid(row=4, column=1)

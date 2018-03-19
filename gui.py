import pprint
from glob import glob
from tkinter import *
from PIL import Image, ImageTk
from threadgenius import ThreadGenius
from threadgenius.types import ImageFileInput, ImageUrlInput
import urllib, cStringIO

class GUI:
    def __init__(self, root, img_path):
        self.threshold = 0.3
        api_key = 'key_MmQxM2Y5M2Q0MDg0MmY2MTc1MjVlYWJmYmYyZDVh'
        self.tg = ThreadGenius(api_key=api_key)
        self.pp = pprint.PrettyPrinter(indent=2, depth=10)
        self.pp = self.pp.pprint
        self.img_path = img_path
        self.img_list = glob(img_path+'/*')
        self.current_img_idx = 0
        self.root = root
        self.root.title("A simple GUI")
        self.build_elements()
    def convert_image(self, img_path):
        img = Image.open(img_path)
        img = img.resize((300, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return img
    def draw_bbox(self, bbox):
        img = Image.open(img_path)
        img = img.resize((300, 300), Image.ANTIALIAS)
    def build_elements(self):
        img = self.convert_image(self.img_list[self.current_img_idx])
        self.original = Label(self.root, image=img)
        self.original.image = img
        self.next = Button(self.root, text='next', command=self.next_img)
        self.previous = Button(self.root, text='previous', command=self.prev_img)
        self.tag = Button(self.root, text='tag', command=self.get_tags)
        self.ss = Button(self.root, text='shop style', command=self.get_ss)
        self.output = Text(self.root, width=2000, text='OUTPUT')
        self.quit = Button(self.root, text='QUIT', command=self.root.quit)
        self.set_grid()
    def set_grid(self):
        self.original.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
        self.next.grid(row=0, column=1)
        self.previous.grid(row=1, column=1)
        self.tag.grid(row=2, column=1)
        self.ss.grid(row=3, column=1)
        self.output.grid(row=0, column=2, sticky=N+E+W+S, rowspan=6, padx=5, pady=5)
        self.quit.grid(row=6, column=1, sticky=N+E+W+S)
    def get_ss(self):
        image = ImageFileInput(file_object=open(self.img_list[self.current_img_idx], 'rb'))
        resp = self.tg.search_by_image(
                catalog_gid='shopstyle',
                image=image,
                n_results=5)
        cat = [(_['object']['metadata'], _['score']) for _ in resp['response']['results'] if _['score']>self.threshold]
        if len(cat)>0:
            imagelabels = []
            f = cStringIO.StringIO(urllib.urlopen(URL).read())
            for x,_ in cat:
                img = Image.open(cStringIO.StringIO(urllib.urlopen(x['thumbnailURL']).read()))
                img = img.resize((50, 50), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                imagelabels.append(img)
    def get_bbox(self):
        image = ImageFileInput(file_object=open(self.img_list[self.current_img_idx], 'rb'))
        resp = tf.detect_image(image)
        box = [(_['category'], _['score'], _['bbox']) for _ in resp['response']['prediction']['data']['detections'] if _['score']>self.threshold]
    def get_tags(self):
        image = ImageFileInput(file_object=open(self.img_list[self.current_img_idx], 'rb'))
        resp = self.tg.tag_image(image)
        out = [(_['type'], _['name'], _['confidence']) for _ in resp['response']['prediction']['data']['tags'] if _['confidence']>self.threshold]
        if len(out)>0:
            out = self.out_format(out)
            self.output.configure(text=out, width=2000)
    def prev_img(self):
        if self.current_img_idx==0:
            return
        self.current_img_idx -= 1
        img = self.convert_image(self.img_list[self.current_img_idx])
        self.original.configure(image=img)
        self.original.image = img
        self.output.config(text='OUTPUT')
    def next_img(self):
        if self.current_img_idx == len(self.img_list) - 1:
            return
        self.current_img_idx += 1
        img = self.convert_image(self.img_list[self.current_img_idx])
        self.original.configure(image=img)
        self.original.image = img
        self.output.config(text='OUTPUT')
    def out_format(self, out):
        fmt = '{:<8}{:<15}{:<10}'
        j = ''
        self.pp(out)
        for x,y,z in out:
            j += fmt.format(x,y,z) + '\n'
        return j

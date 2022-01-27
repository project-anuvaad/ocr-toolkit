#import threading
import multiprocessing
#import queue
from multiprocessing import Queue
#from src.services.train import train_context
#from src.services.get_corpus import corpus_generator, get_chunk
from code import generator,create_image
from config import  PROCESS,OUTPATH
import time
import os


train_queue = Queue() #queue.Queue()
chuck_count = 0

def train_chunk():
    while True:
        ls=(train_queue.get(block=True))
        create_image(ls[0],ls[1],ls[2],ls[3],ls[4],OUTPATH)
def start_threads(thread_count):
    threads = []
    for t in range(thread_count):
        threads.append(multiprocessing.Process(target=train_chunk))
        threads[-1].start()


if __name__ == '__main__':

    os.system('mkdir -p ' +OUTPATH)
    para = generator()
    start_threads(PROCESS)
            
    while True :
        p=False
        while train_queue.qsize() < PROCESS :
            try:
                background,font,symbol,font_size,col = para.__next__()
                ls=[background,font,symbol,font_size,col]
                train_queue.put(ls)
                #time.sleep(.1)
            except StopIteration:
                p=True
                break
            #time.sleep(.1)
            #print('chunks in queue: {}'.format(train_queue.qsize()))
            
        time.sleep(0.05)
        if p:
            break
        
        
    print('Image Generation finished at {}'.format(OUTPATH))
    


    #start_threads(THREADS)
    
    #print('length of corpus is {}'.format(len(corpus)))
    #corpus = corpus[1000000:]
    #while corpus != []:
        #chunk = corpus[:CHUNK_SIZE]
        #train_queue.put(chunk)
        #del corpus[:CHUNK_SIZE]
        #del chunk
        #print('chunks in queue: {}'.format(train_queue.qsize()) )
        #time.sleep(1)

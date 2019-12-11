from PIL import Image
import os

max_frames = 300

def SaveToGif(name, src_dir, dest_dir, extra_frames, replace_old = False):
    if os.path.exists(dest_dir+'{}.gif'.format(name)):
        if (not(replace_old)):
            print('A file already exists with the name {}.gif. GIF creation failed'.format(name))
            return
    if os.path.exists(src_dir+'/steps'):
        parentDir = src_dir+'/steps'
        frames = []
        framecount = 0
        if not os.path.exists(parentDir+'/0.png'):
            print('Error occured while creating gif at:', src_dir,'\nERROR: STARTING FRAME NOT FOUND')
            return
        for i in range(extra_frames):
            frames.append(Image.open(parentDir+'/0.png'))
            framecount+=1
        for framenum in range(1,max_frames + 1):
            if os.path.exists(parentDir+'/{}.png'.format(framenum)):
                frames.append(Image.open(parentDir+'/{}.png'.format(framenum)))
            else:
                for i in range(extra_frames - 1):
                    frames.append(Image.open(parentDir+'/{}.png'.format(framenum - 1)))
                break
        # Save into a GIF file that loops forever
        frames[0].save(dest_dir+'/{}.gif'.format(name), format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)
    else:
        print('Error occured while creating gif at:', src_dir,'\nERROR: STEPS FOLDER NOT FOUND')


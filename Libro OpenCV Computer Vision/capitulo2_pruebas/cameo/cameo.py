import cv2
from managers import WindowManager, CaptureManager

# Inicialmente no grababa el video en disco.
# Para que lo grabase he seguido los pasos que indican aqui:
# https://stackoverflow.com/questions/35242735/can-not-read-or-play-a-video-in-opencvpython-using-videocapture

class Cameo(object):
    
    def __init__(self):
        self._windowManager = WindowManager('Cameo',
                                            self.onKeypress)
        self._captureManager = CaptureManager(
            cv2.VideoCapture(0), self._windowManager, True)
    
    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            
            if frame is not None:
                # TODO: Filter the frame (Chapter 3).
                pass
            
            self._captureManager.exitFrame()
            self._windowManager.processEvents()
    
    def onKeypress(self, keycode):
        """Handle a keypress.
        
        space  -> Take a screenshot.
        tab    -> Start/stop recording a screencast.
        escape -> Quit.
        
        """
        print "keycode=", keycode
       2 if keycode == 32: # space
            self._captureManager.writeImage('screenshot.png')
        elif keycode == 9: # tab
            if not self._captureManager.isWritingVideo:
                print "startWritingVideo"
                self._captureManager.startWritingVideo(
                    'screencast.avi')
            else:
                print "stopWritingVideo"
                self._captureManager.stopWritingVideo()
        elif keycode == 27: # escape
            self._windowManager.destroyWindow()

if __name__=="__main__":
    Cameo().run()

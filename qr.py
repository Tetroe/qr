import cv2
import datetime

class qr():
    def __init__(self):
        ## Holds codes that have been read in this session
        self.bank = []

    ## If QR is a valid value, save it to the bank of codes if its not already there
    def save_qr(self, code: str):
        if (code != False) and (code != ''):
            if code not in self.bank:
                self.bank.append(code)
                print(len(self.bank), code)

    ## Detect the presence of a QR code in an image
    def check_qr(self, img):
        try:
            qrCodeDetector = cv2.QRCodeDetector()
            code, points, _ = qrCodeDetector.detectAndDecode(img)
            if points is not None:
                self.save_qr(code)
        except:
            return
        
    def save_bank(self):
        with open(f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.txt', 'w') as pad:
            [pad.write(f"{x}\n") for x in self.bank]

        
if __name__ == '__main__':
    reader = qr()

    cv2.namedWindow('w')
    vc = cv2.VideoCapture(0)

    while True:
        ## Read camera.
        _, frame = vc.read()

        ## Update display.
        cv2.imshow('w', frame)
        
        ## Check and save QR code if needed.
        reader.check_qr(frame)

        ## Check if a key has been pressed and close the window if so.
        key = cv2.waitKey(10)
        if key != -1:
            break
        
    vc.release()
    cv2.destroyWindow('w')
    reader.save_bank()
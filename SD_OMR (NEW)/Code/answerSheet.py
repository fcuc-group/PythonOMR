from fpdf import FPDF
from qrcode import QRCode
from pdf2image import convert_from_path
import time

def createPDF(subjectId,studentName,studentId,answerlist):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    #put fcuc logo
    pdf.image("./static/image/FCUC_LOGO.png", 60, 10, 88.25, 35.75)

    #create qr code
    qr = QRCode()
    qr.add_data(subjectId+';'+studentName+';'+studentId+';'+answerlist) # set qr data
    img = qr.make_image() # create img
    img.save('qrcode.png') # save it

    #add qrcode to pdf
    pdf.image("qrcode.png", 160, 10, 35.75, 35.75)


    #create text answer sheet
    pdf.set_font("Arial","B", size=20)
    pdf.cell(70, 110, txt="Answer Zone", ln=1, align="C")

    #create answer frame
    pdf.set_line_width(1)
    pdf.rect(20, 70, 55, 211)

    #set answer number text
    pdf.set_font("Arial","B", size=15)

    answerLetters = ["A", "B", "C", "D"]

    #create question number
    pdf.set_line_width(0.5)
    for i in range(20):
        y = 10.4
        y *= i

        pdf.rect(10, 73+y, 8, 8)
        if (i+1) < 10:
            pdf.text(11, 79 + y, txt="0"+str(i+1))
        else:
            pdf.text(11, 79 + y, txt=str(i + 1))

        for j in range(4):
            x = 12
            x *= j
            pdf.ellipse(24.5 + x, 73 + y, 9, 9)
            pdf.text(27 + x, 79 + y, txt=answerLetters[j])

    #create make frame
    pdf.set_line_width(1)
    pdf.rect(90, 70, 100, 40)
    pdf.text(95, 90, txt="Marks: ")

    #create name subject
    textList = ["Name:", "Student Id:", "Subject:", "Course:"]
    pdf.set_line_width(0.5)
    for i in range(4):
        y = 11
        y *= i
        pdf.text(95, 125 + y, txt=textList[i])
        pdf.dashed_line(130, 128 + y, 190, 128 + y, 1, 2)


    # "Honor Pledge for Exams"
    # "I affirm that I will not give or receive any " \
    # "unauthorized help on this exam, and that all" \
    # "work will be my own."
    pdf.text(95, 180, "Honor Pledge for Exams")
    pdf.set_font("Arial", size=15)
    pdf.text(95, 190, "\"I affirm that I will not give or receive any")
    pdf.text(95, 200, "unauthorized help on this exam, and that")
    pdf.text(95, 210, "all work will be my own.\"")


    textList = ["Signature:", "Date:"]
    for i in range(2):
        y = 11
        y *= i
        pdf.text(95, 240 + y, txt=textList[i])
        pdf.dashed_line(130, 240 + y, 190, 240 + y, 1, 2)


    #answerSheetFileName = "./static/uploads/answerSheet/pdf/" + time.strftime("%Y%m%d-%H%M%S", time.localtime())
    answerSheetFileName = "answerSheet/"+time.strftime("%Y%m%d-%H%M%S", time.localtime())
    pdf.output(answerSheetFileName+ ".pdf")
    pdf.close()


    images = convert_from_path(answerSheetFileName+ ".pdf", 100)
    for image in images:
        image.save(answerSheetFileName+'.png')

    return answerSheetFileName+'.png'
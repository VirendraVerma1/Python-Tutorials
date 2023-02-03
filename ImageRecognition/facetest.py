import face_recognition
from face_recognition.api import face_locations

# image= face_recognition.load_image_file('./img/groups/team1.jpg')
# face_locations=face_recognition.face_locations(image)
# print(face_locations)

image_of_bill=face_recognition.load_image_file('./img/known/Bill Gates.jpg')
bill_face_encoding=face_recognition.face_encodings(image_of_bill)[0]

# unknown_image=face_recognition.load_image_file('./img/unknown/bill-gates-4.jpg')
unknown_image=face_recognition.load_image_file('./img/unknown/d-trump.jpg')
unknown_face_encoding=face_recognition.face_encodings(unknown_image)[0]

#compare faces
results=face_recognition.compare_faces([bill_face_encoding],unknown_face_encoding )

if(results[0]):
    print("this is bill gates")
else:
    print("oops")
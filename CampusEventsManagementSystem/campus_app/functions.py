def handle_uploaded_file(f, fileName):  
    with open('static/uploads/'+fileName, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  
def main(parameters):
    # upload_url = "https://hp-heatmap-frontend-44nub6ij6q-ez.a.run.app/"
    #upload_url = "http://hiri-heatmap.test.fedcloud.eu/"
    #upload_url = "http://localhost:1024/"
    upload_url = "http://127.1.1.1:8080/"
    print("heatmap.py")
    print(parameters)
    return upload_url+'?config='+str(parameters["db_entry_id"])

def standar_response(http_status, content, message):
    json = {'status': http_status,
            'content': content,
            'message': message}
    return json

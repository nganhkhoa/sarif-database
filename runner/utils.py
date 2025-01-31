def modify_file(file_path, phrase, replace):
    content = open(file_path).read()
    replaced = content.replace(phrase, replace)
    open(file_path, "w").write(replaced)

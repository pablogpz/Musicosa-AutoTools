from models import EntryExtraInfo, Entry

if __name__ == '__main__':
    # [Each line] Entry title '#' EXTRA INFO
    #   EXTRA INFO -> [0: saga]
    with open("contestant_forms/4th-edition/entries-extra-info.txt", "r", encoding="UTF-8") as file:
        lines = file.readlines()
        entries_extra_info = [line.split("#") for line in lines if "#" in line]

    entries_extra_info_dict = {entry_title.strip(): extra_info.strip()
                               for (entry_title, extra_info) in entries_extra_info}

    for entry_title, extra_info in entries_extra_info_dict.items():
        related_entry = Entry.ORM.get(Entry.ORM.title == entry_title)
        EntryExtraInfo.ORM.create(entry=related_entry, saga=extra_info)

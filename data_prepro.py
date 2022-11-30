import json

class c2s():

    def __init__(self, pair_file_dev, pair_file_test, pair_file_train,
                 data_file_dev, data_file_test, data_file_train,
                 pair , out_true, out_false, json_file):

        self.pair_file = [pair_file_dev,pair_file_test,pair_file_train]
        self.data_file =[data_file_dev,data_file_test,data_file_train]
        self.pair = pair
        self.out_ture = out_true
        self.out_false = out_false
        self.json_file = json_file

    def get_pair(self):
        for file in self.pair_file:
            with open(file, encoding='utf-8') as f:
                self.pair.update(json.load(f))
        return self.pair

    def get_data(self):
        for file in self.data_file:
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
                for line in data:
                    if line.get('label') == 'True' and line.get( "scenario") == 'causal':
                        self.out_ture[str(line.get('id'))] = line.get( "sent")
                    if line.get('label') == 'False' and line.get( "scenario") == 'causal':
                        self.out_false[str(line.get('id'))] = line.get("sent")

        return  self.out_ture, self.out_false


    def out_put(self):
        write = []
        i= 0
        for id, sent in self.out_ture.items():
            i = i+1
            write_sub = {'id' : i, 'True':sent, 'False':self.out_false[self.pair[id]]}
            write.append(write_sub)
        with open(self.json_file, 'w', encoding='utf-8', newline='\n') as fs:
            json.dump(write, fs, ensure_ascii=False,indent=1)
        return write

pair = {}
out_ture = {}
out_false = {}
a = c2s('cs2_convert/data/pair_id_dev.json','cs2_convert/data/pair_id_test.json','cs2_convert/data/pair_id_train.json',
        'cs2_convert/data/dev.json','cs2_convert/data/test.json','cs2_convert/data/train.json',
        pair, out_ture, out_false,'cs2_convert/cs2_convert.json')

pair = a.get_pair()
out = a.get_data()
result = a.out_put()

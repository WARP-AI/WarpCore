import json

class MultiFilter():
    def __init__(self, rules, default=False):
        self.rules = rules
        self.default = default

    def __call__(self, x):
        try:
            x_json = x['json']
            if isinstance(x_json, bytes):
                x_json = json.loads(x_json) 
            validations = []
            for k, r in self.rules.items():
                if isinstance(k, tuple):
                    v = r(*[x_json[kv] for kv in k])
                else:
                    v = r(x_json[k])
                validations.append(v)
            return all(validations)
        except Exception:
            return False

class MultiGetter():
    def __init__(self, rules):
        self.rules = rules

    def __call__(self, x_json):
        if isinstance(x_json, bytes):
            x_json = json.loads(x_json) 
        outputs = []
        for k, r in self.rules.items():
            if isinstance(k, tuple):
                v = r(*[x_json[kv] for kv in k])
            else:
                v = r(x_json[k])
            outputs.append(v)
        if len(outputs) == 1:
            outputs = outputs[0]
        return outputs
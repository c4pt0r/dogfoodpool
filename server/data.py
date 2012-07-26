import redis
import json
import time

class DogFood:
    # redis key prefix
    _key_prefix = 'dogfood'
    _user_key_prefix = 'user'
    _action_key_prefix = 'action'

    _redis = redis.Redis('localhost', 6379)

    def __init__(self, product_name):
        self._pn = product_name

    def _gen_key(self):
        return "%s.%s" % (self._key_prefix , self._pn)

    def _gen_user_key(self, ukey):
        return "%s.%s.%s" % (self._user_key_prefix , self._pn ,  ukey)

    def _gen_action_key(self, action , ukey, day = time.strftime('%Y%m%d') ):
        return "%s.%s.%s.%s.%s" % (self._action_key_prefix, self._pn, action, ukey, day)

    def get_users(self):
        ret = []
        # get dogfood users
        s = self._redis.smembers(self._gen_key())
        # fetch user info
        for name in s:
            item = json.loads(self._redis.get(self._gen_user_key(name)))
            ret.append(item)
        return ret

    def record_action(self, usr_key, action):
        key = self._gen_action_key(action, usr_key)
        print key
        return self._redis.incr(key)

    def get_action_list(self, action , user = '*',  date = '*'):
        key = self._gen_action_key(action, user, date)
        keys = self._redis.keys(key)
        return [{'times' : json.loads(self._redis.get(key)), 'key' : key } for key in keys]

    def add_user(self, usr_key, usr_info = {}):
        if usr_key is None or len(usr_key) == 0: return False
        if self._redis.sadd(self._gen_key(), usr_key) > 0:
            # dog food info
            usr_info['key'] = usr_key
            usr_info['is_enable'] = True
            usr_info['date'] = time.time()
            # set!
            self._redis.set(self._gen_user_key(usr_key) , json.dumps(usr_info))
            return True
        return False

    def is_user_enable(self, usr_key):
        try:
            info = json.loads(self._redis.get(self._gen_user_key(usr_key)))
            return info['is_enable']
        except:
            return False

    def toggle_user_enable_status(self, usr_key):
        info = json.loads(self._redis.get(self._gen_user_key(usr_key)))
        info['is_enable'] = not info['is_enable']
        return self._redis.set(self._gen_user_key(usr_key), json.dumps(info))

class DogFoodPool:
    _redis = redis.Redis('localhost')
    _product_prefix = 'products'
    def add_product(self, pn):
        self._redis.hset("%s.%s" %(self._product_prefix, pn), 'enable', 1)

    def remove_product(self,pn):
        self._redis.hset('%s.%s' %(self._product_prefix, pn), 'enable', 0)

    def get_product_list(self):
        keys = self._redis.keys(self._product_prefix + '*')
        return [item.split('.')[1] for item in keys]

    def get_product(self, pn):
        if not self._redis.exists('%s.%s' % (self._product_prefix, pn)):
            return None
        is_enable = self._redis.hget('%s.%s' %(self._product_prefix, pn), 'enable')
        if is_enable == 0:
            return None
        return DogFood(pn)

    def restore_product(self, pn):
        pass

pool = DogFoodPool()

def dogfoodproduct(name):
    return pool.get_product(name)


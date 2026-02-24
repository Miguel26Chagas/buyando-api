import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

r.setex("codigo_teste", 5, "123456")

r.set('foo', 'bar')

# print(f"Código no Redis: {r.get('codigo_teste').decode('utf-8')}")

# print("Esperando 6 segundos...")
# time.sleep(6)

# print(f"Código após 6 segundos: {r.get('codigo_teste')}") 

print(r.get('codigo_teste'))
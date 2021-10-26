import time

import persona_trainer

start_time = time.time()

print("Training Tom...")
persona_trainer.train_model("Tom")
think_time = time.time() - start_time
start_time = time.time()
print("Tom trained in {} seconds".format(think_time))

print("Training Jerry...")
persona_trainer.train_model("Jerry")
think_time = time.time() - start_time
start_time = time.time()
print("Jerry trained in {} seconds".format(think_time))

print("Training Tweety...")
persona_trainer.train_model("Tweety")
think_time = time.time() - start_time
start_time = time.time()
print("Tweety trained in {} seconds".format(think_time))

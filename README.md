# FLAPPY BIRD - REINFORECEMENT LEARNING #

### Environment:

* Python: 3.10
* pip: 22.3.1

### Create virtualenv

* Install virtualenv:
```properties
pip install virtualenv
```
* Create virtual environment:
```properties
virtualenv venv
```
* Activate virtual environment:
```properties
source venv/bin/activate
```
* Install all dependencies:
```properties
pip install -r requirements.txt
```
### Training arguments
 - --num_episodes: number of episodes
 - --td_type: Temporal difference types, possible are: SARSA, QLearning, EMA QLeaning
 - --action_selection: Action selection type; possible are: Greedy, E-Greedy
 - --alpha
 - --gamma
 - --epsilon
 - --epsilon-decay: float, default is None
 - --epsilon_min: minimization of epsilon, used when epsilon_decay is not None
 - --mu: used when TD type is EMA Qlearning.
 - --log_dir: log path

### Train agent
```properties
run run_train.sh
```

### Test agent
```properties
run run_test.sh
```

(*) Change the path of checkpoint file if needed
python train.py \
    --num_episodes 1000 \
    --td_type "sarsa" \
    --action_selection "greedy" \
    --alpha 0.1 \
    --gamma 0.9 \
    --epsilon 0.9 \
    --log_dir "exp1" \
    # --epsilon-decay 0.999 \
    # --epsilon_min 0.01 \
    # --mu 0.4 \
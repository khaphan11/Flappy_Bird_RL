python train.py \
    --num_episodes 2000 \
    --td_type "qlearning" \
    --action_selection "greedy" \
    --alpha 0.1 \
    --gamma 0.9 \
    --epsilon 0.9 \
    --log_dir "qlearning" \
    # --epsilon-decay 0.999 \
    # --epsilon_min 0.01 \
    # --mu 0.4 \
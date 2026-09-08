def predict_delivery_risk(crew_size, days_remaining, tasks_left):
    efficiency = tasks_left / (crew_size * days_remaining)

    if efficiency > 1.5:
        return "High risk"
    elif efficiency > 0.8:
        return "Medium risk"
    else:
        return "Low risk"


print(predict_delivery_risk(3, 5, 25))
print(predict_delivery_risk(4, 10, 18))
print(predict_delivery_risk(2, 4, 8))

# Code Challenge 2: The Simp Detector.
print("\nThe Simp Detector:\n")


def simp_alert(money_spent, texts_sent, texts_replied, dates_asked, dates_accepted):
    reply_rate = texts_replied / texts_sent
    date_rate = dates_accepted / dates_asked
    score = (reply_rate + date_rate) / 2

    if score >= 0.5:
        return "She likes you"
    elif score >= 0.2:
        return "Lukewarm"
    else:
        return "You are simping"


print(simp_alert(60, 15, 2, 6, 0))
print(simp_alert(200, 30, 18, 5, 2))
print(simp_alert(120, 20, 8, 4, 1))

import pandas as pd
import matplotlib.pyplot as plt
from crypto_utils import generate_key, encrypt_value, decrypt_value
from blockchain_utils import build_blockchain, verify_blockchain


def load_data():
    return pd.read_csv("data/students.csv")


def classify_risk(score):
    if score >= 4:
        return "Alto"
    if score >= 2:
        return "Medio"
    return "Bajo"


def generate_recommendation(student):
    actions = []

    if student["grade"] < 5:
        actions.append("refuerzo academico")
    if student["participation"] < 50:
        actions.append("aumentar participacion")
    if student["assignments_submitted"] < 7:
        actions.append("seguimiento de entregas")
    if student["absences"] > 4:
        actions.append("contacto por absentismo")

    if not actions:
        return "Mantener seguimiento normal"

    return "Priorizar " + ", ".join(actions)


def add_learning_analytics_metrics(data):
    data = data.copy()

    data["risk_score"] = (
        (data["grade"] < 5) * 2
        + (data["participation"] < 50)
        + (data["assignments_submitted"] < 7)
        + (data["absences"] > 4)
    )

    data["risk_level"] = data["risk_score"].apply(classify_risk)
    data["recommendation"] = data.apply(generate_recommendation, axis=1)
    return data


def basic_analysis(data):
    print("\nResumen de Learning Analytics")
    print("-----------------------------")

    total_students = len(data)
    average_grade = data["grade"].mean()
    average_participation = data["participation"].mean()
    average_absences = data["absences"].mean()
    pass_rate = (data["grade"] >= 5).mean() * 100
    at_risk_students = data[data["risk_level"].isin(["Medio", "Alto"])]

    print("Numero total de estudiantes:", total_students)
    print("Nota media:", round(average_grade, 2))
    print("Participacion media:", round(average_participation, 2), "%")
    print("Ausencias medias:", round(average_absences, 2))
    print("Porcentaje de aprobados:", round(pass_rate, 2), "%")
    print("Estudiantes con riesgo medio o alto:", len(at_risk_students))

    print("\nNota media por curso:")
    grades_by_course = data.groupby("course")["grade"].mean().sort_values(ascending=False)
    for course, grade in grades_by_course.items():
        print(f"{course}: {round(grade, 2)}")

    print("\nDistribucion de riesgo:")
    risk_distribution = data["risk_level"].value_counts()
    for level, count in risk_distribution.items():
        print(f"{level}: {count}")

    print("\nRecomendaciones personalizadas:")
    for _, student in data.iterrows():
        print(
            f"{student['student_id']} - {student['name']} "
            f"({student['risk_level']}): {student['recommendation']}"
        )


def show_grade_chart(data):
    average_grade_by_course = data.groupby("course")["grade"].mean().sort_values(ascending=False)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(average_grade_by_course.index, average_grade_by_course.values)

    plt.title("Nota media por curso")
    plt.xlabel("Curso")
    plt.ylabel("Nota media")
    plt.ylim(0, 10)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, round(height, 2),
                 ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig("output/average_grade_by_course.png")
    plt.show()


def show_risk_chart(data):
    risk_order = ["Bajo", "Medio", "Alto"]
    risk_distribution = data["risk_level"].value_counts().reindex(risk_order, fill_value=0)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(risk_distribution.index, risk_distribution.values)

    plt.title("Distribucion de riesgo academico")
    plt.xlabel("Nivel de riesgo")
    plt.ylabel("Numero de estudiantes")

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, int(height),
                 ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig("output/risk_distribution.png")
    plt.show()


def show_participation_chart(data):
    sorted_data = data.sort_values("participation", ascending=False)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(sorted_data["student_id"], sorted_data["participation"])

    plt.title("Participacion por estudiante")
    plt.xlabel("Estudiante")
    plt.ylabel("Participacion (%)")
    plt.ylim(0, 100)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, int(height),
                 ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig("output/participation_by_student.png")
    plt.show()


def test_encryption(data):
    print("\nPrueba de cifrado")
    print("-----------------")

    key = generate_key()

    original_value = str(data.iloc[0]["name"])
    encrypted_value = encrypt_value(original_value, key)
    decrypted_value = decrypt_value(encrypted_value, key)

    print("Valor original:", original_value)
    print("Valor cifrado:", encrypted_value)
    print("Valor descifrado:", decrypted_value)


def test_blockchain(data):
    print("\nPrueba de integridad con hash")
    print("-----------------------------")

    blockchain = build_blockchain(data)

    print("Primer bloque:")
    print(blockchain[0])

    is_valid = verify_blockchain(blockchain)
    print("\nLa cadena es valida?:", is_valid)

    print("\nSimulamos que alguien consigue modificar su nota")
    blockchain[1]["grade"] = 10

    is_valid_after_change = verify_blockchain(blockchain)
    print("La cadena sigue siendo valida despues del cambio?:", is_valid_after_change)


def main():
    data = load_data()
    data = add_learning_analytics_metrics(data)
    basic_analysis(data)
    show_grade_chart(data)
    show_risk_chart(data)
    show_participation_chart(data)
    test_encryption(data)
    test_blockchain(data)


if __name__ == "__main__":
    main()

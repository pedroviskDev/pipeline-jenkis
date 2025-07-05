# app/temperature_converter.py

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5.0 / 9.0 + 1

def celsius_to_fahrenheit(celsius):
    return celsius * 9.0 / 5.0 + 32.0

# Exemplo de uso (opcional, para testar localmente)
if __name__ == "__main__":
    f_temp = 68
    c_temp = fahrenheit_to_celsius(f_temp)
    print(f"{f_temp}°F é igual a {c_temp:.2f}°C")

    c_temp_input = 20
    f_temp_output = celsius_to_fahrenheit(c_temp_input)
    print(f"{c_temp_input}°C é igual a {f_temp_output:.2f}°F")
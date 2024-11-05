import json
import os

EMPLOYEES_FILE = "employees.json"
PROJECTS_FILE = "projects.json"
DEPARTMENTS_FILE = "departments.json"

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def create_department():
    departments = load_data(DEPARTMENTS_FILE)
    nome = input("Digite o nome do departamento: ")
    numero = input("Digite o número do departamento: ")
    gerente_cpf = input("Digite o CPF do gerente do departamento: ")

    for department in departments:
        if department["nome"] == nome:
            print("Nome do departamento já existe.")
            return
        if department["numero"] == numero:
            print("Número do departamento já existe.")
            return

    department_id = len(departments) + 1
    departments.append({
        "id": department_id,
        "nome": nome,
        "numero": numero,
        "gerente_cpf": gerente_cpf,
        "projetos": []
    })
    save_data(DEPARTMENTS_FILE, departments)
    print(f"\nDepartamento {nome} criado com sucesso!")

def create_project():
    projects = load_data(PROJECTS_FILE)
    departments = load_data(DEPARTMENTS_FILE)
    
    name = input("Digite o nome do projeto: ")
    number = input("Digite o número do projeto: ")
    place = input("Digite o local do projeto: ")
    department_id = int(input("Digite o ID do departamento que controla o projeto: "))

    for project in projects:
        if project["nome"] == name:
            print("Nome do projeto já existe.")
            return
        if project["numero"] == number:
            print("Número do projeto já existe.")
            return

    if not any(department["id"] == department_id for department in departments):
        print("Departamento não encontrado.")
        return

    project_id = len(projects) + 1
    projects.append({
        "id": project_id,
        "nome": name,
        "numero": number,
        "local": place,
        "departamento_id": department_id
    })
    save_data(PROJECTS_FILE, projects)

    for department in departments:
        if department["id"] == department_id:
            department["projetos"].append(project_id)
            save_data(DEPARTMENTS_FILE, departments)
            break

    print(f"\nProjeto {name} criado com sucesso!")

def create_employee():
    employees = load_data(EMPLOYEES_FILE)
    projects = load_data(PROJECTS_FILE)
    departments = load_data(DEPARTMENTS_FILE)

    first_name = input("Digite o primeiro nome do funcionário: ")
    inicial_medium_name = input("Digite a inicial do nome do meio: ")
    last_name = input("Digite o último nome do funcionário: ")
    cpf = input("Digite o CPF do funcionário: ")
    address = input("Digite o endereço do funcionário: ")
    salary = float(input("Digite o salário do funcionário: "))
    gender = input("Digite o gênero do funcionário: ")
    birthday = input("Digite a data de nascimento do funcionário (YYYY-MM-DD): ")
    department_id = int(input("Digite o ID do departamento do funcionário: "))
    project_ids = input("Digite os IDs dos projetos (separados por vírgula): ").split(",")

    for employee in employees:
        if employee["cpf"] == cpf:
            print("CPF já existe.")
            return

    if not any(department["id"] == department_id for department in departments):
        print("Departamento não encontrado.")
        return

    employee_projects = []
    for project_id in project_ids:
        project_id = int(project_id.strip())
        if any(project["id"] == project_id for project in projects):
            employee_projects.append(project_id)
        else:
            print(f"Projeto com ID {project_id} não encontrado. Ignorando.")

    employee_id = len(employees) + 1
    employees.append({
        "id": employee_id,
        "primeiro_nome": first_name,
        "inicial_meio": inicial_medium_name,
        "ultimo_nome": last_name,
        "cpf": cpf,
        "endereco": address,
        "salario": salary,
        "genero": gender,
        "data_nascimento": birthday,
        "departamento_id": department_id,
        "projetos": employee_projects
    })
    save_data(EMPLOYEES_FILE, employees)
    print(f"\nFuncionário {first_name} {last_name} criado com sucesso!")

def main():
    while True:
        print("\nBem-vindo ao sistema de cadastro!\n")
        print("1 - Criar Departamento")
        print("2 - Criar Projeto")
        print("3 - Criar Funcionário")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            create_department()
        elif opcao == "2":
            create_project()
        elif opcao == "3":
            create_employee()
        else:
            print("Opção inválida.")

        print("\nDeseja realizar outro cadastro?\n")
        print("1 - Sim")
        print("2 - Não")
        continuar = input("Escolha uma opção: ")
        
        if continuar != "1":
            print("Encerrando o sistema de cadastro.")
            break

if __name__ == "__main__":
    main()
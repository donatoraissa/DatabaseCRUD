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

def read_departments():
    departments = load_data(DEPARTMENTS_FILE)
    projects = load_data(PROJECTS_FILE)

    if not departments:
        print("Nenhum departamento encontrado.")
        return
    
    for dept in departments:
        project_names = [proj["nome"] for proj in projects if proj["id"] in dept["projetos"]]
        print(f"ID: {dept['id']}, Nome: {dept['nome']}, Número: {dept['numero']}, Gerente CPF: {dept['gerente_cpf']}, Projetos: {project_names}")

def read_projects():
    projects = load_data(PROJECTS_FILE)
    departments= load_data(DEPARTMENTS_FILE)

    if not projects:
        print("Nenhum projeto encontrado.")
        return
    
    for proj in projects:
        dept_name = next((dept["nome"] for dept in departments if dept["id"] == proj["departamento_id"]), "Departamento não encontrado")
        print(f"ID: {proj['id']}, Nome: {proj['nome']}, Número: {proj['numero']}, Local: {proj['local']}, Departamento ID: {proj['departamento_id']}, Departamento: {dept_name}")

def read_employees():
    employees = load_data(EMPLOYEES_FILE)
    departments = load_data(DEPARTMENTS_FILE)
    projects = load_data(PROJECTS_FILE)

    if not employees:
        print("Nenhum funcionário encontrado.")
        return
    
    for emp in employees:
        dept_name = next((dept["nome"] for dept in departments if dept["id"] == emp["departamento_id"]), "Departamento não encontrado")
        project_names = [proj["nome"] for proj in projects if proj["id"] in emp["projetos"]]
        print(f"ID: {emp['id']}, Nome: {emp['primeiro_nome']} {emp['inicial_meio']} {emp['ultimo_nome']}, CPF: {emp['cpf']}, Endereço: {emp['endereco']}, Salário: {emp['salario']}, Gênero: {emp['genero']}, Nascimento: {emp['data_nascimento']}, Departamento: {dept_name}, Projetos: {project_names}")

def update_department():
    departments = load_data(DEPARTMENTS_FILE)
    department_id = int(input("Digite o ID do departamento que deseja atualizar: "))

    for department in departments:
        if department["id"] == department_id:
            print(f"Atualizando o departamento: {department['nome']}")
            nome = input(f"Novo nome ({department['nome']}): ") or department["nome"]
            numero = input(f"Novo número ({department['numero']}): ") or department["numero"]
            gerente_cpf = input(f"Novo CPF do gerente ({department['gerente_cpf']}): ") or department["gerente_cpf"]

            department["nome"] = nome
            department["numero"] = numero
            department["gerente_cpf"] = gerente_cpf

            save_data(DEPARTMENTS_FILE, departments)
            print("Departamento atualizado com sucesso!")
            return

    print("Departamento não encontrado.")

def update_project():
    projects = load_data(PROJECTS_FILE)
    project_id = int(input("Digite o ID do projeto que deseja atualizar: "))

    for project in projects:
        if project["id"] == project_id:
            print(f"Atualizando o projeto: {project['nome']}")
            nome = input(f"Novo nome ({project['nome']}): ") or project["nome"]
            numero = input(f"Novo número ({project['numero']}): ") or project["numero"]
            local = input(f"Novo local ({project['local']}): ") or project["local"]
            department_id = int(input(f"Novo ID do departamento ({project['departamento_id']}): ") or project["departamento_id"])

            project["nome"] = nome
            project["numero"] = numero
            project["local"] = local
            project["departamento_id"] = department_id

            save_data(PROJECTS_FILE, projects)
            print("Projeto atualizado com sucesso!")
            return

    print("Projeto não encontrado.")

def update_employee():
    employees = load_data(EMPLOYEES_FILE)
    employee_id = int(input("Digite o ID do funcionário que deseja atualizar: "))

    for employee in employees:
        if employee["id"] == employee_id:
            print(f"Atualizando o funcionário: {employee['primeiro_nome']} {employee['ultimo_nome']}")
            first_name = input(f"Novo primeiro nome ({employee['primeiro_nome']}): ") or employee["primeiro_nome"]
            inicial_medium_name = input(f"Nova inicial do meio ({employee['inicial_meio']}): ") or employee["inicial_meio"]
            last_name = input(f"Novo último nome ({employee['ultimo_nome']}): ") or employee["ultimo_nome"]
            cpf = input(f"Novo CPF ({employee['cpf']}): ") or employee["cpf"]
            address = input(f"Novo endereço ({employee['endereco']}): ") or employee["endereco"]
            salary = float(input(f"Novo salário ({employee['salario']}): ") or employee["salario"])
            gender = input(f"Novo gênero ({employee['genero']}): ") or employee["genero"]
            birthday = input(f"Nova data de nascimento ({employee['data_nascimento']}): ") or employee["data_nascimento"]
            department_id = int(input(f"Novo ID do departamento ({employee['departamento_id']}): ") or employee["departamento_id"])
            project_ids = input("Novos IDs dos projetos (separados por vírgula): ").split(",") or employee["projetos"]

            employee["primeiro_nome"] = first_name
            employee["inicial_meio"] = inicial_medium_name
            employee["ultimo_nome"] = last_name
            employee["cpf"] = cpf
            employee["endereco"] = address
            employee["salario"] = salary
            employee["genero"] = gender
            employee["data_nascimento"] = birthday
            employee["departamento_id"] = department_id
            employee["projetos"] = [int(proj_id.strip()) for proj_id in project_ids]

            save_data(EMPLOYEES_FILE, employees)
            print("Funcionário atualizado com sucesso!")
            return

    print("Funcionário não encontrado.")

def delete_department():
    departments = load_data(DEPARTMENTS_FILE)
    department_id = int(input("Digite o ID do departamento que deseja deletar: "))

    departments = [department for department in departments if department["id"] != department_id]

    save_data(DEPARTMENTS_FILE, departments)
    print("Departamento deletado com sucesso!")

def delete_project():
    projects = load_data(PROJECTS_FILE)
    project_id = int(input("Digite o ID do projeto que deseja deletar: "))

    projects = [project for project in projects if project["id"] != project_id]

    save_data(PROJECTS_FILE, projects)
    print("Projeto deletado com sucesso!")

def delete_employee():
    employees = load_data(EMPLOYEES_FILE)
    employee_id = int(input("Digite o ID do funcionário que deseja deletar: "))

    employees = [employee for employee in employees if employee["id"] != employee_id]

    save_data(EMPLOYEES_FILE, employees)
    print("Funcionário deletado com sucesso!")

def main():
    while True:
        print("\n1. Criar Departamento")
        print("2. Criar Projeto")
        print("3. Criar Funcionário")
        print("4. Visualizar Departamentos")
        print("5. Visualizar Projetos")
        print("6. Visualizar Funcionários")
        print("7. Atualizar Departamento")
        print("8. Atualizar Projeto")
        print("9. Atualizar Funcionário")
        print("10. Deletar Departamento")
        print("11. Deletar Projeto")
        print("12. Deletar Funcionário")
        print("0. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            create_department()
        elif choice == "2":
            create_project()
        elif choice == "3":
            create_employee()
        elif choice == "4":
            read_departments()
        elif choice == "5":
            read_projects()
        elif choice == "6":
            read_employees()
        elif choice == "7":
            update_department()
        elif choice == "8":
            update_project()
        elif choice == "9":
            update_employee()
        elif choice == "10":
            delete_department()
        elif choice == "11":
            delete_project()
        elif choice == "12":
            delete_employee()
        elif choice == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()


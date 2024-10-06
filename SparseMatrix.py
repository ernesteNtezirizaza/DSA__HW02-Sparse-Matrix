class SparseMatrix:
    def __init__(self, num_rows, num_cols):
        """
        Initializes a SparseMatrix object.

        :param num_rows: Number of rows in the matrix
        :param num_cols: Number of columns in the matrix
        """
        self.elements = {}
        self.num_rows = num_rows
        self.num_cols = num_cols

    @staticmethod
    def _parse_matrix_file(file_path):
        """
        Parses the matrix file manually without using built-in libraries for path handling.

        :param file_path: Path to the matrix file
        :return: List of lines from the matrix file
        """
        try:
            with open(file_path.replace("\\", "/"), "r") as file:
                lines = file.readlines()
                return [line.strip() for line in lines if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def from_file(matrix_file_path):
        """
        Loads a sparse matrix from the given file.

        :param matrix_file_path: The path of the file containing matrix data
        :return: SparseMatrix instance
        """
        lines = SparseMatrix._parse_matrix_file(matrix_file_path)
        
        if len(lines) < 2:
            raise ValueError(f"File {matrix_file_path} must contain at least two lines for dimensions.")
        
        # Parse the matrix dimensions
        try:
            num_rows = int(lines[0].split('=')[1])
            num_cols = int(lines[1].split('=')[1])
        except (IndexError, ValueError):
            raise ValueError(f"Invalid matrix dimensions in {matrix_file_path}.")
        
        matrix = SparseMatrix(num_rows, num_cols)

        # Parse matrix elements
        for line in lines[2:]:
            if not line.startswith("(") or not line.endswith(")"):
                raise ValueError(f"Invalid format for matrix element: {line}")

            elements = line[1:-1].split(',')
            try:
                row = int(elements[0].strip())
                col = int(elements[1].strip())
                value = int(elements[2].strip())
            except (IndexError, ValueError):
                raise ValueError(f"Invalid matrix element format in file: {line}")
            
            matrix.set_element(row, col, value)
        
        return matrix

    def set_element(self, row, col, value):
        """
        Sets a value at a specific row and column in the sparse matrix.

        :param row: Row index
        :param col: Column index
        :param value: Value to set
        """
        if row >= self.num_rows:
            self.num_rows = row + 1
        if col >= self.num_cols:
            self.num_cols = col + 1
        
        key = f"{row},{col}"
        self.elements[key] = value

    def get_element(self, row, col):
        """
        Gets a value from a specific row and column in the sparse matrix.

        :param row: Row index
        :param col: Column index
        :return: Value at the given row and column, or 0 if no element is present
        """
        key = f"{row},{col}"
        return self.elements.get(key, 0)

    def add(self, other):
        """
        Adds two sparse matrices and returns the result.

        :param other: SparseMatrix to add
        :return: A new SparseMatrix instance representing the result of the addition
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError(f"Cannot add matrices of different dimensions.")
        
        result = SparseMatrix(self.num_rows, self.num_cols)
        
        # Add elements of this matrix
        for key, value in self.elements.items():
            row, col = map(int, key.split(','))
            result.set_element(row, col, value)

        # Add elements from the other matrix
        for key, value in other.elements.items():
            row, col = map(int, key.split(','))
            result.set_element(row, col, result.get_element(row, col) + value)
        
        return result

    def subtract(self, other):
        """
        Subtracts one sparse matrix from another.

        :param other: SparseMatrix to subtract
        :return: A new SparseMatrix instance representing the result of the subtraction
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError(f"Cannot subtract matrices of different dimensions.")
        
        result = SparseMatrix(self.num_rows, self.num_cols)
        
        # Subtract elements of other matrix
        for key, value in other.elements.items():
            row, col = map(int, key.split(','))
            result.set_element(row, col, self.get_element(row, col) - value)
        
        return result

    def multiply(self, other):
        """
        Multiplies two sparse matrices.

        :param other: SparseMatrix to multiply
        :return: A new SparseMatrix instance representing the result of the multiplication
        """
        if self.num_cols != other.num_rows:
            raise ValueError(f"Cannot multiply: column count of the first matrix must equal row count of the second.")
        
        result = SparseMatrix(self.num_rows, other.num_cols)

        for key1, value1 in self.elements.items():
            row1, col1 = map(int, key1.split(','))
            for key2, value2 in other.elements.items():
                row2, col2 = map(int, key2.split(','))
                if col1 == row2:
                    result.set_element(row1, col2, result.get_element(row1, col2) + value1 * value2)
        
        return result

    def __str__(self):
        """
        Returns a string representation of the sparse matrix.

        :return: String representation of the matrix
        """
        result = [f"rows={self.num_rows}", f"cols={self.num_cols}"]
        for key, value in self.elements.items():
            row, col = key.split(',')
            result.append(f"({row}, {col}, {value})")
        return '\n'.join(result)

    def save_to_file(self, file_path):
        """
        Saves the sparse matrix to a file.

        :param file_path: Path to save the matrix
        """
        with open(file_path, 'w') as file:
            file.write(str(self))


def get_user_input(prompt):
    """
    Gets user input from the console.

    :param prompt: The prompt to display
    :return: User input as a string
    """
    return input(prompt)


def do_some_operations():
    """
    Performs matrix operations based on user input.
    """
    try:
        operations = {
            'A': ('addition', 'add'),
            'B': ('subtraction', 'subtract'),
            'C': ('multiplication', 'multiply')
        }

        print("MATRIX Operations: ")
        print("(A) Addition")
        print("(B) Subtraction")
        print("(C) Multiplication")

        choice = get_user_input("Choose operation (A,B,C): ")
        if choice not in operations:
            raise ValueError("Invalid option.")

        file1 = get_user_input("Enter path for the first matrix file: ")
        file2 = get_user_input("Enter path for the second matrix file: ")

        print(f"Loading first matrix from {file1}...")
        matrix1 = SparseMatrix.from_file(file1)
        print(f"Loaded matrix of size {matrix1.num_rows}x{matrix1.num_cols} successfully")

        print(f"Loading second matrix from {file2}...")
        matrix2 = SparseMatrix.from_file(file2)
        print(f"Loaded matrix of size {matrix2.num_rows}x{matrix2.num_cols} successfully")

        operation_name, method = operations[choice]
        print(f"Performing {operation_name}...")

        result = getattr(matrix1, method)(matrix2)
        output_file = f"{operation_name}_output.txt"
        result.save_to_file(output_file)

        print(f"Operation completed successfully. Output saved to {output_file}.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    do_some_operations()
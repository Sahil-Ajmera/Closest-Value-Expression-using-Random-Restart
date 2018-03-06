"""
Author : Sahil Ajmera
Program to find the closest value expression for the given target value as input
"""
from random import *
import time


class best_expression:

    def generate_list(self,target):
        """
        Generating the starting expression for each iteration of the Random Restart
        :return:Starting expression in a list
        """
        expression_list = []
        operator_list = ['+', '-', '/', '*']

        # Initializing the list
        for i in range(199):
            expression_list.append(0)

        operand_list = [3, 3, 7, 3, 3, 4, 6, 7, 3, 5, 8, 2, 7, 6, 4, 4, 1, 2, 2, 8, 3, 2, 3, 0, 2, 3, 3, 7, 7, 3, 2, 9, 0, 2, 0, 4, 3, 0, 2, 7, 1, 3, 7, 1, 7, 0, 7, 8, 4, 1, 9, 9, 2, 3, 5, 0, 4, 9, 1, 4, 6, 0, 1, 1, 4, 5, 1, 9, 7, 4, 5, 3, 7, 2, 9, 7, 2, 0, 1, 8, 1, 4, 3, 9, 3, 5, 3, 6, 6, 8, 9, 7, 7, 9, 4, 6, 7, 1, 6, 6]

        shuffle(operand_list,random)
        pointer_to_operand_list = 0
        # Initializing the list with operators and operands
        for i in range(199):

            # Putting operands at even position in the list
            if i % 2 == 0:
                expression_list[i] = operand_list[pointer_to_operand_list]
                pointer_to_operand_list = pointer_to_operand_list + 1

            # Putting operators at odd positions in the list
            else:
                expression_list[i] = operator_list[int(random()*4)]
        string = ''

        for value in expression_list:
            string = string + str(value)
        print('Start expression:'+string+'='+str(self.compute_function_value(expression_list,target)))
        return expression_list

    def evaluate_list(self, list):
        """
        Evaluating a particular expression supplied to this function
        :param list:list containing a certain expression supplied to the function
        :return:Value on computing the expression
        """
        stack = []
        op1 = list[0]
        # Putting first element in stack
        stack.append(op1)
        oper = ''

        # Updating the stack
        for i in range(1,len(list)):
            if isinstance(list[i],int):
                if oper is '+':
                    stack[0] = stack[0] + list[i]
                elif oper is '-':
                    stack[0] = stack[0] - list[i]
                elif oper is '*':
                    stack[0] = stack[0] * list[i]

                # Avoding the /0 condition
                elif oper is '/' and list[i]!=0:
                    stack[0] = stack[0] / list[i]
            else:
                oper = list[i]
        return stack[0]

    def compute_function_value(self,list,target):
        """
        Computing the object function value for the expression.Objective function helps in movement from one state to another
        :param list:Expression whose objective function value needs to be computed.
        :param target:Final desired value
        :return:Objective function value for a particular expression
        """
        list_value= self.evaluate_list(list)
        return target - list_value

    def check_successors(self,list,target):
        """
        One iteration of random restart
        :param list:Expression
        :param target:Final desired value
        :return:list with the least objective function value alongwith the value
        """
        parent_min_value = abs(self.compute_function_value(list,target))
        temp_list = list
        min_value = abs(self.compute_function_value(list,target))
        copy_list = list

        # While a lower objective function value is possible
        while True:

            # Operation swap on a list
            for temp_list_from_swap in self.swap(temp_list):
                computed_value=abs(self.compute_function_value(temp_list_from_swap,target))
                if computed_value < min_value:
                    min_value = computed_value
                    temp_list = temp_list_from_swap
            temp_list_2 = copy_list

            # Operation change_op on a list
            for temp_list_from_change_op in self.change_op(temp_list_2):
                computed_value = abs(self.compute_function_value(temp_list_from_change_op,target))
                if computed_value < min_value:
                    min_value = computed_value
                    temp_list = temp_list_from_change_op

            # If no expression formed as a result of swap or change op, has a better result than the parent exrpression
            if min_value==parent_min_value:
                string =''
                for value in temp_list:
                    string=string+str(value)
                print('Best state in this iteration:'+string+'='+str(min_value))
                return temp_list,min_value
            else:
                string = ''
                for value in temp_list:
                    string = string + str(value)
                print(string + '=' + str(min_value))
                parent_min_value = min_value
                copy_list = temp_list

    def swap(self,list):
        """
        Swap operation on the expression
        :param list:expression provided
        :return:list of list which contain new expressions formed as a result of swap
        """
        list_formed = []

        # Take all expression that can be formed  from the swap operation on the expression
        for i in range(0, len(list), 2):
            for j in range(0, len(list), 2):
                temp_list = list[:]
                if i != j:
                    temp_list[i],temp_list[j] = temp_list[j],temp_list[i]
                    if temp_list not in list_formed:
                        list_formed.append(temp_list)
        return list_formed

    def change_op(self,list):
        """
        change operator operation on the expression
        :param list:expression provided
        :return:list of list which contain new expressions formed as a result of change of operator
        """
        list_formed = []

        # List of possible operators
        op_list = ['+', '*', '/', '-']
        for operator_index in range(1, len(list), 2):
            for i in op_list:
                temp_list = list[:]
                if i != list[operator_index]:
                    temp_list[operator_index] = i
                    if temp_list not in list_formed:
                        list_formed.append(temp_list)

        return list_formed


def main():
    """
    Main executing function
    :return:None
    """
    class_obj = best_expression()
    target_value = int(input('Enter the target value for the 100 numbers'))
    timeout_value = int(input('Enter the value of time for your program'))

    # Taking program timeout into consideration
    start_time = time.time()
    end_time = start_time + timeout_value

    best_value = 1000000000000000000000000000000000000000000000000000000000000
    best_list = []

    while start_time < end_time:
        final_list,final_value = class_obj.check_successors(class_obj.generate_list(target_value),target_value)
        if best_value > final_value and final_value != 0:
            best_value = final_value
            best_list = final_list

        # If goal is reached then break
        elif final_value == 0:
            best_value = final_value
            best_list = final_list
            break
        print('\n')
        start_time = time.time()
    string = ''
    for value in final_list:
        string = string + str(value)
    print('\n')
    print("Best expression:"+string + "="+str(best_value))


if __name__ == "__main__":
    main()






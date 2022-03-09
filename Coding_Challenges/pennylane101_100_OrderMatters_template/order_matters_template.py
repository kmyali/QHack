#! /usr/bin/python3
# cat 2.in | python order_matters_template.py
import sys
import pennylane as qml
from pennylane import numpy as np


def compare_circuits(angles):
    """Given two angles, compare two circuit outputs that have their order of operations flipped: RX then RY VERSUS RY then RX.

    Args:
        - angles (np.ndarray): Two angles

    Returns:
        - (float): | < \sigma^x >_1 - < \sigma^x >_2 |
    """

    # QHACK #

    # define a device and quantum functions/circuits here
    dev1 = qml.device("default.qubit", wires=2)

    @qml.qnode(dev1)
    def circuit1(angles):
        qml.RX(angles[0], wires=0)
        qml.RY(angles[1], wires=0)
        return qml.expval(qml.PauliX(0))

    @qml.qnode(dev1)
    def circuit2(angles):
        qml.RY(angles[1], wires=1)
        qml.RX(angles[0], wires=1)
        return qml.expval(qml.PauliX(1))
    
    drawCircuits(angles, [circuit1, circuit2])

    result = circuit1(angles) - circuit2(angles)
    return np.absolute(result)

def drawCircuits(angles, circuits):
    for circuit in circuits:
        drawer1 = qml.draw(circuit) 
        print(drawer1(angles))
    

if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    angles = np.array(sys.stdin.read().split(","), dtype=float)
    output = compare_circuits(angles)
    print(f"{output:.6f}")

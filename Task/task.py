from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_distribution

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler

token = 'a90ef2bb7af2b3444b1df3b42112a7b0e016fd7785f7ffb5502b1fe940ba83ceebba89ada1c78a10adb18aca7911bce50dcda425adb3f1cab451e5bb2f1ad48c'

service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

def grover_oracle(marked_states):
    if not isinstance(marked_states, list):
        marked_states = [marked_states]
    num_qubits = len(marked_states[0])

    qc = QuantumCircuit(num_qubits)
    for target in marked_states:
        rev_target = target[::-1]
        zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
        qc.x(zero_inds)
        qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
        qc.x(zero_inds)
    return qc

marked_states = ["011", "100"]

oracle = grover_oracle(marked_states)
oracle.draw(output="mpl", style="iqp")

print(oracle)

grover_op = GroverOperator(oracle)
grover_op.decompose().draw(output="mpl", style="iqp")

print(grover_op)

# optimal_num_iterations = math.floor(
#     math.pi / (4 * math.asin(math.sqrt(len(marked_states) / 2**grover_op.num_qubits)))
# )

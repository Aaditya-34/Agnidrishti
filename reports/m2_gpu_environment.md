\# M2 GPU Environment



\## Branch



\- Branch: `m2/gpu-annotation`



\## Hardware



\- GPU: NVIDIA GeForce RTX 3050 6GB Laptop GPU

\- VRAM: 6144 MiB



\## Software



\- OS: Windows

\- Python: 3.12.9

\- NVIDIA Driver: 581.86

\- NVIDIA-SMI CUDA Version: 13.0



\## PyTorch



\- PyTorch: 2.14.0+cu126

\- PyTorch CUDA Runtime: 12.6

\- CUDA available: True

\- GPU detected by PyTorch: NVIDIA GeForce RTX 3050 6GB Laptop GPU



\## GPU Inference Test



Command:



```text

python -c "import torch; x=torch.rand(5000,5000,device='cuda'); y=x@x; torch.cuda.synchronize(); print('Result device:', y.device); print('GPU:', torch.cuda.get\_device\_name(0)); print('Allocated VRAM:', round(torch.cuda.memory\_allocated(0)/1024\*\*2,2), 'MB')"


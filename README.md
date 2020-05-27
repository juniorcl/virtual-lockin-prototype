# Virtual Lock-in Prototype
This a virtual lock-in prototype which is still in development. This project were made in python during my master's degree in natural sciences at the at the State University of Northern Fluminense Darcy Ribeiro.

## Getting Started
This project woked in a photoacoustic spectroscopy experiment. Brieafly, it takes the noise signal and applies the [lock-in](https://www.thinksrs.com/downloads/pdfs/manuals/SR830m.pdf) funtion. As a result the lock-in function returns x and y, they atr saved in a csv file. These values can be used to calculate the value of R and &theta;. Finally the program plots the R-values which is the amplitude of the filtered signal.

### Usage
We used in our photoacoustic laboratory studies with equipaments. Therefore, there are some libraries dependencies. The noise and reference signal are get from audio card. Each signal can be get from each channel. Below  there are all the libraries used in this project.

### Dependencies
- [NumPy](https://numpy.org/)
- [PyVisa](https://pyvisa.readthedocs.io/en/latest/)
- [SciPy](https://www.scipy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Drawnow](https://github.com/stsievert/python-drawnow)

## Acknowledgment
- State University of Northern Fluminense Darcy Ribeiro ([UENF](http://uenf.br/))
- Graduate Program in Natural Sciences ([PGCN](http://uenf.br/posgraduacao/ciencias-naturais/))

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


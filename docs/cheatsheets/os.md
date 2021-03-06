
## Profiling
 * https://wiki.freebsd.org/DTrace
 * https://wiki.freebsd.org/PmcTools


### Linux (SO_REUSEPORT)

 * https://lwn.net/Articles/542629/


### Linux (perf)


http://www.berniepope.id.au/linuxPerfEvents.html



	sudo perf record -g -e cycles,cache-misses,branch-misses,stalled-cycles-frontend,stalled-cycles-backend `which wstest` -m testeeserver -w ws://127.0.0.1:9000

	sudo perf report

#### Install from package

	sudo apt-get install linux-tools-common 
	sudo apt-get install linux-tools
	sudo apt-get install linux-tools-3.8.0-32

#### Build from source

	sudo apt-get install -y libelf-dev
	sudo apt-get install -y binutils-dev
	sudo apt-get install -y libdwarf-dev
	sudo apt-get install -y flex
	sudo apt-get install -y bison
	sudo apt-get install -y libunwind-dev
	sudo apt-get install -y elfutils
	sudo apt-get install -y libdw-dev
	sudo apt-get install -y libaudit-dev
	sudo apt-get install -y libslang-dev
	sudo apt-get install -y libgtk2.0-dev
	sudo apt-get install -y libnuma-dev

	wget https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.11.tar.bz2
	cd linux-3.11/tools/perf/

	export PREFIX=$HOME/local
	export PYTHON=$HOME/local/bin/python2.7
	export LD_LIBRARY_PATH=$HOME/local/lib

	make
	make install


sudo /home/oberstet/build/linux-3.11/tools/perf/perf record ..
sudo /home/oberstet/build/linux-3.11/tools/perf/perf script -g python



Record:
sudo ~/build/linux-3.11/tools/perf/perf record -a --event raw_syscalls:sys_enter

Generate template:
sudo ~/build/linux-3.11/tools/perf/perf script -g python

Analyze:
sudo ~/build/linux-3.11/tools/perf/perf script -s perf-script.py




 * http://www.jauu.net/data/pdf/cpu-profiling.pdf

 * http://www.linuxtag.org/2013/fileadmin/www.linuxtag.org/slides/Arnaldo_Melo_-_Linux__perf__tools__Overview_and_Current_Developments.e323.pdf
 * http://en.wikipedia.org/wiki/Perf_%28Linux%29
 * https://perf.wiki.kernel.org/index.php/Main_Page
 * https://perf.wiki.kernel.org/index.php/Tutorial
 * http://www.pixelbeat.org/programming/profiling/
 * http://penberg.blogspot.co.uk/2009/06/jato-has-profiler.html
 * http://lists.freedesktop.org/archives/mesa-dev/2013-April/037952.html
 * http://web.eece.maine.edu/~vweaver/projects/perf_events/
 * http://stackoverflow.com/questions/12697028/profiling-output-of-jit-on-linux-with-perf-events-oprofile
 * http://stackoverflow.com/questions/tagged/perf
 * http://git.kernel.org/cgit/linux/kernel/git/tip/tip.git/tree/tools/perf
 * http://git.kernel.org/cgit/linux/kernel/git/tip/tip.git/tree/tools/perf/Documentation/perf-script-python.txt
 * http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=80d496be89ed7dede5abee5c057634e80a31c82d

## Health Monitoring

 * http://dtrace.org/blogs/brendan/2012/02/29/the-use-method/
 * http://dtrace.org/blogs/brendan/2012/03/07/the-use-method-linux-performance-checklist/
 * http://dtrace.org/blogs/brendan/2013/09/25/the-use-method-freebsd-performance-checklist/


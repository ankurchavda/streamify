echo "Downloading Java..."
cd ~
mkdir spark
cd spark
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz

echo "Exporting Java Path..."
echo '' >> ~/.bashrc
echo 'export JAVA_HOME="${HOME}/spark/jdk-11.0.2"' >> ~/.bashrc
echo 'export PATH="${JAVA_HOME}/bin:${PATH}"' >> ~/.bashrc

eval "$(cat ~/.bashrc | tail -n +10)" # A hack because source .bashrc doesn't work inside the script

echo "Installed Java version is..."
java --version

rm openjdk-11.0.2_linux-x64_bin.tar.gz

echo "Downloading Spark..."
wget https://dlcdn.apache.org/spark/spark-3.0.3/spark-3.0.3-bin-hadoop3.2.tgz

echo "Extracting Spark..."
tar xzfv spark-3.0.3-bin-hadoop3.2.tgz
rm spark-3.0.3-bin-hadoop3.2.tgz

echo "Exporting Spark Home..."
echo '' >> ~/.bashrc
echo 'export SPARK_HOME="${HOME}/spark/spark-3.0.3-bin-hadoop3.2"' >> ~/.bashrc
echo 'export PATH="${SPARK_HOME}/bin:${PATH}"' >> ~/.bashrc
eval "$(cat ~/.bashrc | tail -n +10)" # A hack because source .bashrc doesn't work inside the script


echo "Setting up Pyspark"
#Get correct name for py4j library
py4j="$(basename ${SPARK_HOME}/python/lib/py4j*)"
echo "py4j versions is $py4j"

echo '' >> ~/.bashrc
echo 'export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"' >> ~/.bashrc
echo 'export PYTHONPATH="${SPARK_HOME}/python/lib/${!py4j}:$PYTHONPATH"' >> ~/.bashrc
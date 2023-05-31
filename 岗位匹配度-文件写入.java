import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class ResultCsvMapReduce {

    // Mapper类
    public static class ResultCsvMapper extends Mapper<Object, Text, Text, FloatWritable> {

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            // 解析CSV行数据
            String[] columns = value.toString().split(",");
            // 提取需要的列数据
            float score1 = Float.parseFloat(columns[0]); 
            float score2 = Float.parseFloat(columns[1]); 
            float score3 = Float.parseFloat(columns[2]); 
			float score4 = Float.parseFloat(columns[3]);
			float score5 = Float.parseFloat(columns[4]);
			float score6 = Float.parseFloat(columns[5]);

            // 计算加权求和并生成新列数据
            float newCol = score1 * 0.1f + score2 * 0.15f + score3 * 0.1f + score4 * 0.05f + score5 * 0.1f + score6 * 0.5f; // 根据实际需求计算加权求和

            // 将新列数据写入Context，作为Mapper阶段的输出
            context.write(new Text("岗位匹配度"), new FloatWritable(newCol));
        }
    }

    // Reducer类
    public static class ResultCsvReducer extends Reducer<Text, FloatWritable, Text, FloatWritable> {

        @Override
        public void reduce(Text key, Iterable<FloatWritable> values, Context context)
                throws IOException, InterruptedException {
            // 对Mapper阶段输出的相同Key的Value进行归并并求和
            float sum = 0;
            for (FloatWritable value : values) {
                sum += value.get();
            }

            // 将最终的求和结果作为Reducer阶段的输出
            context.write(key, new FloatWritable(sum));
        }
    }

    public static void main(String[] args) throws Exception {
        // 创建配置对象
        Configuration conf = new Configuration();
        // 创建Job对象
        Job job = Job.getInstance(conf, "ResultCsvMapReduce");
        job.setJarByClass(ResultCsvMapReduce.class);

        // 设置Mapper和Reducer类
        job.setMapperClass(ResultCsvMapper.class);
        job.setReducerClass(ResultCsvReducer.class);

        // 设置Mapper和Reducer的输出键值对类型
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(FloatWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(FloatWritable.class);

        // 设置输入路径和输出路径
        FileInputFormat.addInputPath(job, new Path(args[0])); // 输入文件路径
        FileOutputFormat.setOutputPath(job, new Path(args[1])); // 输出文件路径

        // 提交作业并等待完成
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

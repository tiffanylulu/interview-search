"""
从「最新-宝典新版.docx」提取后端面试题 Q&A
来源标记为"官方文档"，岗位为"后端开发"
"""
import json, os, re
from docx import Document

DOC_PATH = r'F:\桌面简文\最新-宝典新版.docx'
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'baodian_questions.json')

doc = Document(DOC_PATH)
all_lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

# 手动定义面试题及其答案边界
# 格式: (title_pattern, is_question_func, answer_start_pattern)
# 基于对文档内容的分析，逐题提取

questions = []
qid = 0

def add_q(position, difficulty, title, answer, tags, source="官方文档"):
    global qid
    qid += 1
    desc = title  # 题目即描述
    return {
        "position": position,
        "difficulty": difficulty,
        "source": source,
        "publishDate": "2024-06-01",
        "title": title,
        "description": desc,
        "answer": answer.strip(),
        "tags": tags
    }

# ==== SECTION 1: Java 基础 ====
java_basic = [
    ("JDK 和 JRE 有什么区别？", "初级", ["Java基础", "JDK", "JRE"],
     "JDK（Java Development Kit）是Java开发工具包，提供了Java的开发环境和运行环境。JRE（Java Runtime Environment）是Java运行环境。JDK包含JRE，同时还包含编译器javac及调试分析工具。运行Java程序只需JRE，开发Java程序需要JDK。"),
    
    ("抽象类与接口的区别？", "中级", ["Java基础", "抽象类", "接口"],
     "1) 抽象类可以有构造方法，接口不能有。2) 抽象类可以有普通成员变量，接口中的变量默认是public static final常量。3) 抽象类可以包含非抽象方法，接口中的方法在Java 8之前都是抽象的（Java 8后可以有default/static方法）。4) 一个类只能继承一个抽象类，但可以实现多个接口。5) 抽象类体现继承关系（is-a），接口体现行为契约（has-a）。"),
    
    ("== 和 equals 的区别是什么？", "初级", ["Java基础", "运算符", "equals"],
     "== 是运算符，equals是Object类的方法。对于基本数据类型：== 比较存储的值。对于引用数据类型：== 比较所指向对象的地址值；equals默认比较地址值，但String等类重写了equals方法，比较的是对象的内容是否相等。"),
    
    ("final 在 Java 中有什么作用？", "初级", ["Java基础", "final"],
     "final可以修饰类、方法和变量。final修饰的类不能被继承（如String类）。final修饰的方法不能被重写。final修饰的变量是常量，必须初始化，初始化后值不可修改。"),
    
    ("final、finally、finalize 的区别？", "初级", ["Java基础", "关键字对比"],
     "final是修饰符（关键字），修饰类/方法/变量使其不可变。finally用于try-catch语句中，表示最终总会执行的代码块（通常用于关闭资源）。finalize是Object类的方法，在对象被GC回收前调用（已不推荐使用，Java 9标记为deprecated）。"),
    
    ("String 类的常用方法有哪些？", "初级", ["Java基础", "String"],
     "equals()字符串比较；indexOf()返回指定字符索引；charAt()返回指定索引字符；replace()字符串替换；trim()去除两端空白；split()分割字符串；getBytes()返回byte数组；length()返回长度；substring()截取；toLowerCase()/toUpperCase()大小写转换。"),
    
    ("String、StringBuilder、StringBuffer 的区别？", "中级", ["Java基础", "字符串"],
     "1) 可变性：String不可变（final char[]），StringBuilder和StringBuffer可变。2) 线程安全：StringBuffer是线程安全的（synchronized），StringBuilder非线程安全。3) 性能：StringBuilder > StringBuffer > String。少量数据用String；多线程大量数据用StringBuffer；单线程大量数据用StringBuilder。"),
    
    ("Java 反射机制是什么？", "中级", ["Java基础", "反射"],
     "Java反射机制指在运行时动态获取类的信息，创建对象、调用方法和访问属性的技术。主要涉及：Class类（类的元数据）、Method类（方法元数据）、Field类（属性元数据）、Constructor类（构造函数元数据）。反射是动态代理（Proxy）的底层支撑，也是Spring IOC/DI的核心基础。"),
    
    ("常见的异常类有哪些？", "初级", ["Java基础", "异常"],
     "NullPointerException空指针；ClassNotFoundException指定类不存在；NumberFormatException字符串转数字异常；IndexOutOfBoundsException数组下标越界；ClassCastException类型转换异常；FileNotFoundException文件未找到；NoSuchMethodException方法不存在；IOException IO异常；SocketException Socket异常。"),
    
    ("Java 中异常处理机制？", "中级", ["Java基础", "异常处理"],
     "异常分为受检异常（Checked Exception，编译时检查，如IOException）和非受检异常（Unchecked Exception，运行时异常，如NullPointerException）。处理关键字：try包裹可能异常的代码；catch捕获处理异常（可有多个）；finally无论是否异常都执行（关闭资源）；throw主动抛出异常。SpringMVC中使用@ControllerAdvice + @ExceptionHandler统一处理。"),
    
    ("实例化对象有哪几种方式？", "初级", ["Java基础", "对象创建"],
     "1) new关键字：最常见的方式。2) clone()方法：实现Cloneable接口并重写clone()。3) 反序列化：实现Serializable接口。4) 工厂模式：通过工厂类创建对象，避免直接new。5) 反射：Class.newInstance()或Constructor.newInstance()。"),
    
    ("重载与重写的区别？", "初级", ["Java基础", "多态"],
     "重载（Overload）：同一个类中，方法名相同但参数列表不同（类型/个数/顺序），返回值可同可不同，编译时多态。重写（Override）：子类对父类方法的重新实现，方法名、参数列表、返回值必须相同，运行时多态。重写方法访问权限不能比父类更严格，不能抛出比父类更多的异常。"),
    
    ("深拷贝与浅拷贝的区别？", "中级", ["Java基础", "拷贝"],
     "浅拷贝：仅拷贝基本类型变量值和引用类型变量的地址值，引用指向的堆中对象不会拷贝（共享同一对象）。深拷贝：完全拷贝，包括引用类型变量指向的堆中对象也复制一份（完全独立）。实现深拷贝可通过实现Cloneable接口递归clone、序列化反序列化、或手动new对象赋值。"),
    
    ("int 和 Integer 有什么区别？什么是自动拆装箱？", "初级", ["Java基础", "包装类"],
     "int是基本数据类型，Integer是int的包装类（引用类型）。装箱：将基本类型转成包装类（Integer.valueOf(int)）。拆箱：将包装类转成基本类型（Integer.intValue()）。自动拆装箱是Java 5引入的编译器特性，编译器自动完成转换。Integer默认值是null，int默认值是0。Integer有缓存池（-128到127）。"),
    
    ("break、continue、return 的区别及作用？", "初级", ["Java基础", "流程控制"],
     "break：跳出整个循环，不再执行循环体。continue：跳出本次循环，继续执行下次循环。return：结束当前方法，返回调用处，不再执行方法内后续代码。"),
    
    ("Java 中常见的基本排序算法？", "初级", ["Java基础", "排序"],
     "冒泡排序：相邻元素两两比较，大的往后移，O(n²)。选择排序：每次选择未排序部分最小值放到已排序末尾，O(n²)。插入排序：将未排序元素插入已排序序列合适位置，O(n²)。快速排序：选基准值，分区递归排序，O(nlog n)。归并排序：分治法，先分后合并，O(nlog n)。记住冒泡和选择即可应对初级面试。"),
]

for title, diff, tags, answer in java_basic:
    questions.append(add_q("后端开发", diff, title, answer, tags))

# ==== SECTION 2: Java 容器/集合 ====
java_collection = [
    ("数组和集合的区别？", "初级", ["容器", "数组", "集合"],
     "1) 长度：数组长度固定，集合长度可变。2) 存储类型：数组可存基本类型+引用类型；集合只能存引用类型（基本类型需用包装类）。3) 数组随机访问性能更强O(1)，集合（如LinkedList）插入删除更高效。"),
    
    ("ArrayList 和 LinkedList 区别？", "中级", ["容器", "ArrayList", "LinkedList"],
     "1) 底层结构：ArrayList基于动态数组，LinkedList基于双向链表。2) 内存占用：LinkedList更占内存（节点需存储前后引用）。3) 访问：随机访问ArrayList O(1)优于LinkedList O(n)；插入删除LinkedList O(1)优于ArrayList O(n)（需移动元素）。4) ArrayList适合频繁读取，LinkedList适合频繁增删。"),
    
    ("List、Set、Map 的区别？", "初级", ["容器", "集合框架"],
     "List和Set实现了Collection接口，Map是独立接口。List：有序可重复，允许多个null，常用ArrayList/LinkedList/Vector。Set：无序不可重复，最多一个null，常用HashSet/TreeSet。Map：键值对存储，键唯一且最多一个null键，值可重复允许多个null。常用HashMap/TreeMap/ConcurrentHashMap。"),
    
    ("HashMap 的工作原理？", "中级", ["容器", "HashMap"],
     "JDK 1.8之前：数组+链表。JDK 1.8之后：数组+链表+红黑树。存储：put时计算key的hashCode→高位运算→取模得到数组索引→存入。哈希冲突：链表法，当链表长度>8且数组长度>=64时转为红黑树。扩容：负载因子0.75，容量达到阈值时扩容为2倍，rehash。线程不安全，多线程可用ConcurrentHashMap。"),
    
    ("HashMap 和 HashTable 区别？", "中级", ["容器", "HashMap", "HashTable"],
     "1) 线程安全：HashMap非线程安全，HashTable线程安全（Synchronized）。2) null：HashMap允许null键（一个）和null值（多个）；HashTable不允许null键值。3) 默认容量：HashMap初始16，HashTable初始11。4) 扩容：HashMap扩2倍，HashTable扩2倍+1。5) HashMap要求容量为2的整数次幂，HashTable不要求。"),
    
    ("HashMap 和 ConcurrentHashMap 区别？", "高级", ["容器", "并发"],
     "1) 线程安全：HashMap非线程安全；ConcurrentHashMap线程安全。2) JDK 1.7：ConcurrentHashMap采用分段锁（Segment），并发度16。3) JDK 1.8：改为CAS+synchronized，对单个Node加锁，并发度更高。4) ConcurrentHashMap不允许null键值。5) 遍历：ConcurrentHashMap是弱一致性迭代器。推荐高并发场景使用ConcurrentHashMap。"),
    
    ("HashSet 的实现原理？", "初级", ["容器", "HashSet"],
     "HashSet基于HashMap实现，元素作为HashMap的key存储，value是一个固定的Object常量（PRESENT）。add()方法实际调用HashMap.put(e, PRESENT)，通过HashMap的key唯一性保证元素不重复。"),
    
    ("Vector 是线程安全的吗？", "初级", ["容器", "Vector", "线程安全"],
     "Vector是线程安全的，所有方法都加了synchronized。但性能较差，已不推荐使用。替代方案：使用Collections.synchronizedList(new ArrayList<>())或CopyOnWriteArrayList。"),
    
    ("Map 集合的几种遍历方式？", "初级", ["容器", "Map遍历"],
     "1) keySet()获取key的Set，通过key遍历。2) values()获取所有value遍历。3) entrySet()获取Set<Map.Entry>，通过Iterator遍历。4) foreach + lambda遍历entrySet。5) 迭代器遍历（线程安全场景）。推荐使用entrySet方式，一次获取key和value效率最高。"),
]

for title, diff, tags, answer in java_collection:
    questions.append(add_q("后端开发", diff, title, answer, tags))

# ==== SECTION 3: JVM ====
jvm = [
    ("JVM 内存结构是怎样的？", "中级", ["JVM", "内存模型"],
     "JVM内存结构包括：堆（Heap）：存储对象实例和数组，GC主要区域，线程共享。方法区（Method Area/Metaspace）：存储类信息、常量、静态变量，JDK8后改为元空间（直接内存）。虚拟机栈（VM Stack）：每个线程私有，存储局部变量、操作数栈、方法返回地址。本地方法栈：类似虚拟机栈，服务Native方法。程序计数器：记录当前线程执行字节码行号。"),
    
    ("堆和栈的区别？", "中级", ["JVM", "堆栈"],
     "1) 存储内容：堆存储new创建的对象实例和数组；栈存储局部变量、方法参数、返回地址。2) 管理方式：堆由程序员管理（GC回收）；栈由编译器自动管理。3) 空间大小：堆空间大；栈空间小。4) 存取速度：堆较慢；栈较快。5) 内存连续性：堆不连续；栈连续。6) 数据共享：堆不共享；栈线程私有。"),
    
    ("JVM 的 GC 垃圾回收机制？", "高级", ["JVM", "GC"],
     "GC是自动内存管理机制，流程：1) 标记阶段：遍历对象，标记存活/死亡。2) 清除阶段：回收死亡对象占用的内存。3) 整理阶段：压缩存活对象减少内存碎片。垃圾回收算法：标记-清除（Mark-Sweep）、标记-整理（Mark-Compact）、复制算法（Copying，新生代使用）、分代收集（主流方案）。新生代使用Minor GC，老年代使用Major GC/Full GC。"),
    
    ("类加载过程是怎样的？", "中级", ["JVM", "类加载"],
     "类加载分为5个阶段：1) 加载：通过类全限定名获取二进制字节流，生成Class对象。2) 验证：确保字节码符合JVM规范（文件格式/元数据/字节码/符号引用验证）。3) 准备：为类变量（static）分配内存并赋默认零值。4) 解析：将符号引用替换为直接引用。5) 初始化：执行类构造器<clinit>()，初始化静态变量和静态代码块。"),
    
    ("Java 内存溢出和内存泄漏的区别？", "中级", ["JVM", "内存问题"],
     "内存溢出（OOM）：程序申请内存超过JVM最大限制。解决：增大-Xmx/-Xms参数；优化代码减少内存占用。内存泄漏（Memory Leak）：已分配的内存无法被GC回收。常见原因：长生命周期对象持有短生命周期对象引用；静态集合类未清理；未关闭的资源（连接/流）；ThreadLocal未remove。排查工具：jmap、MAT、VisualVM。"),
]

for title, diff, tags, answer in jvm:
    questions.append(add_q("后端开发", diff, title, answer, tags))

# ==== SECTION 4: 多线程 ====
thread = [
    ("线程和进程的区别？", "初级", ["多线程", "基础概念"],
     "进程是操作系统资源分配的最小单位，线程是CPU调度的最小单位。一个进程可包含多个线程，线程共享进程的内存空间（堆、方法区），但每个线程有独立的栈和程序计数器。进程间通信复杂（IPC），线程间通信简单（共享内存）。进程切换开销大，线程切换开销小。"),
    
    ("Runnable 和 Callable 的区别？", "初级", ["多线程", "接口对比"],
     "1) Runnable的run()方法无返回值，不能抛出受检异常；Callable的call()方法有返回值（泛型），可以抛出异常。2) Runnable通过Thread或线程池执行；Callable通过线程池submit()返回Future，通过Future.get()获取结果。3) Callable配合FutureTask可实现异步获取结果。"),
    
    ("ThreadLocal 的原理和应用场景？", "高级", ["多线程", "ThreadLocal"],
     "原理：每个Thread内部维护一个ThreadLocalMap，key是ThreadLocal的弱引用，value是线程私有的变量副本。应用场景：1) 线程上下文信息传递（如用户登录信息）。2) 线程安全的对象复用（如SimpleDateFormat）。3) 数据库连接管理（每个线程绑定独立连接）。4) 跨层级数据透传。注意：使用后需调用remove()防止内存泄漏。"),
    
    ("volatile 关键字的作用？", "中级", ["多线程", "volatile"],
     "volatile是轻量级同步机制：1) 保证可见性：一个线程修改volatile变量后立即刷新到主内存，其他线程读取时从主内存获取最新值。2) 禁止指令重排序：通过内存屏障实现。3) 不保证原子性：volatile不能替代synchronized，对i++这样的复合操作仍需加锁。适用场景：状态标记变量、双重检查锁的单例模式。"),
    
    ("synchronized 和 volatile 的区别？", "中级", ["多线程", "同步机制"],
     "1) volatile是轻量级，仅保证可见性和有序性；synchronized是重量级，保证原子性、可见性和有序性。2) volatile仅修饰变量；synchronized可修饰方法、代码块。3) volatile不会造成线程阻塞；synchronized会造成线程阻塞。4) volatile不能替代synchronized用于复合操作。5) synchronized性能在JDK 1.6后大幅优化（偏向锁→轻量锁→重量锁升级）。"),
    
    ("synchronized 和 Lock 的区别？", "中级", ["多线程", "锁"],
     "1) synchronized是JVM内置关键字，Lock是java.util.concurrent.locks接口。2) synchronized自动释放锁；Lock需手动unlock（finally块中）。3) Lock可以尝试非阻塞获取锁（tryLock）、可中断获取锁（lockInterruptibly）、超时获取锁。4) synchronized非公平锁；ReentrantLock可指定公平/非公平。5) Lock可通过Condition精准唤醒线程。"),
    
    ("线程池的核心参数有哪些？", "中级", ["多线程", "线程池"],
     "ThreadPoolExecutor的7个参数：1) corePoolSize：核心线程数。2) maximumPoolSize：最大线程数。3) keepAliveTime：非核心线程空闲存活时间。4) unit：时间单位。5) workQueue：阻塞队列（ArrayBlockingQueue/LinkedBlockingQueue/SynchronousQueue）。6) threadFactory：线程工厂。7) handler：拒绝策略（AbortPolicy/CallerRunsPolicy/DiscardPolicy/DiscardOldestPolicy）。"),
]

for title, diff, tags, answer in thread:
    questions.append(add_q("后端开发", diff, title, answer, tags))

# ==== SECTION 5: MySQL ====
mysql = [
    ("数据库的三范式是什么？", "初级", ["MySQL", "设计规范"],
     "1NF：列不可再分，每列都是原子值。2NF：在1NF基础上，非主键列完全依赖于主键（消除部分依赖）。3NF：在2NF基础上，非主键列不依赖于其他非主键列（消除传递依赖）。实际开发中有时会适当反范式化以提升查询性能。"),
    
    ("MySQL 默认存储引擎是什么？InnoDB 与 MyISAM 区别？", "初级", ["MySQL", "存储引擎"],
     "MySQL 5.5+默认引擎是InnoDB。区别：1) InnoDB支持事务（ACID）和行级锁，MyISAM不支持。2) InnoDB支持外键，MyISAM不支持。3) InnoDB聚集索引（数据即索引），MyISAM非聚集索引。4) InnoDB支持MVCC，高并发性能好。5) MyISAM支持全文索引（5.6后InnoDB也支持），读速度快但不适合频繁写。6) InnoDB崩溃恢复能力强（redo log）。"),
    
    ("数据库事务是什么？ACID 特性？", "中级", ["MySQL", "事务"],
     "事务是一组不可分割的数据库操作序列，要么全部成功，要么全部失败。ACID：Atomicity原子性（操作不可分割，通过undo log保证）；Consistency一致性（事务前后数据满足约束）；Isolation隔离性（并发事务互不干扰，通过MVCC和锁保证）；Durability持久性（提交后数据永久保存，通过redo log保证）。"),
    
    ("事务的隔离级别有哪些？", "中级", ["MySQL", "事务隔离"],
     "1) READ UNCOMMITTED：读未提交，存在脏读/不可重复读/幻读。2) READ COMMITTED：读已提交，解决脏读，存在不可重复读/幻读（Oracle默认）。3) REPEATABLE READ：可重复读，解决脏读/不可重复读，存在幻读（MySQL InnoDB默认，通过MVCC+间隙锁解决大部分幻读）。4) SERIALIZABLE：串行化，完全解决，性能最差。"),
    
    ("数据库索引是什么？索引的类型？", "中级", ["MySQL", "索引"],
     "索引是帮助数据库高效获取数据的数据结构（B+树为主）。类型：1) 主键索引（聚集索引）：数据按主键顺序存储。2) 唯一索引：值必须唯一。3) 普通索引：加速查询。4) 联合索引：多列组合索引，遵循最左前缀原则。5) 全文索引：文本搜索。6) 覆盖索引：查询列都在索引中，避免回表。索引虽提升查询速度，但降低写入性能、占用存储空间。"),
    
    ("索引失效的场景有哪些？", "中级", ["MySQL", "索引优化"],
     "1) 使用LIKE '%xxx'（前导模糊）。2) 对索引列使用函数或表达式。3) 使用OR连接的条件中有一个不是索引列。4) 类型隐式转换（如varchar列用数字查询）。5) 联合索引不满足最左前缀原则。6) 使用!=、<>、NOT IN、NOT EXISTS。7) IS NULL或IS NOT NULL（部分情况下）。8) 全表扫描比索引更快时（优化器选择）。"),
    
    ("数据库 SQL 优化方法有哪些？", "高级", ["MySQL", "SQL优化"],
     "1) 避免SELECT *，只查需要的列。2) 合理使用索引，避免索引失效。3) 使用EXPLAIN分析执行计划。4) 大表JOIN时小表驱动大表。5) 分页优化：深分页使用子查询+ID范围。6) IN和EXISTS：外表大用EXISTS，内表大用IN。7) 批量操作代替循环单条。8) 使用连接池（HikariCP/Druid）。9) 分库分表（水平/垂直拆分）。10) 合理使用缓存（Redis）。"),
    
    ("delete、drop、truncate 区别？", "初级", ["MySQL", "删除操作"],
     "1) DELETE：删除表中数据，可加WHERE条件，逐行删除记日志，可回滚，触发器会执行，不释放空间。2) TRUNCATE：快速清空表数据，不可回滚（DDL），重置自增ID，释放空间（drop+create）。3) DROP：删除整个表结构+数据，不可回滚，释放空间。执行速度：DROP > TRUNCATE > DELETE。"),
    
    ("LEFT JOIN、RIGHT JOIN、INNER JOIN 区别？", "初级", ["MySQL", "JOIN"],
     "INNER JOIN（内连接）：只返回两表匹配的行。LEFT JOIN（左外连接）：返回左表全部行，右表不匹配的补NULL。RIGHT JOIN（右外连接）：返回右表全部行，左表不匹配的补NULL。FULL OUTER JOIN（全外连接）：返回两表全部行，不匹配的补NULL（MySQL不直接支持，可用LEFT JOIN UNION RIGHT JOIN实现）。"),
    
    ("MySQL 如何实现高可用？", "高级", ["MySQL", "高可用"],
     "1) 主从复制：一主多从，读写分离，binlog同步。2) MHA/Orchestrator：自动故障检测+主从切换。3) MGR（MySQL Group Replication）：多主模式，Paxos协议保证一致性。4) 分库分表：MyCat/ShardingSphere中间件。5) 中间件高可用：Haproxy + Keepalived做VIP漂移。6) 云数据库：RDS自带高可用方案。"),
    
    ("MySQL 中的日志类型有哪些？", "中级", ["MySQL", "日志"],
     "1) binlog（二进制日志）：记录所有DDL和DML操作（逻辑日志），用于主从复制和数据恢复。2) redo log（重做日志）：InnoDB引擎层，物理日志，保证持久性，crash recovery。3) undo log（回滚日志）：记录数据修改前的版本，保证原子性和MVCC。4) error log（错误日志）：记录MySQL服务启停和错误信息。5) slow query log（慢查询日志）：记录超过long_query_time的SQL。6) relay log（中继日志）：从库用于重放主库的binlog。"),
    
    ("MySQL 主从同步原理？", "高级", ["MySQL", "主从复制"],
     "1) 主库将变更写入binlog。2) 从库的IO线程连接主库，读取binlog并写入relay log。3) 从库的SQL线程读取relay log并重放执行。同步方式：异步复制（默认，可能丢数据）、半同步复制（至少一个从库确认）、全同步复制（所有从库确认，MGR）。全量同步：主库dump+从库load；增量同步：binlog持续同步。"),
]

for title, diff, tags, answer in mysql:
    questions.append(add_q("后端开发", diff, title, answer, tags))

# ==== SECTION 6: Spring 全家桶 ====
spring = [
    ("Spring 的主要模块有哪些？", "初级", ["Spring", "框架"],
     "Spring框架6大模块：1) Core Container（核心容器）：Beans、Core、Context、SpEL。2) AOP：面向切面编程。3) Data Access/Integration：JDBC、ORM、Transactions。4) Web：Spring MVC、WebSocket。5) Messaging：消息支持。6) Test：单元测试和集成测试支持。"),
    
    ("Spring IOC 是什么？依赖注入的方式有几种？", "中级", ["Spring", "IOC"],
     "IOC（控制反转）是将对象的创建和依赖关系的管理交给Spring容器。DI（依赖注入）是IOC的实现方式：1) 构造器注入：通过构造方法注入依赖（推荐，强制依赖）。2) Setter注入：通过setter方法注入（可选依赖）。3) 字段注入：通过@Autowired注解直接注入字段（不推荐，不利于测试）。Spring默认Bean是单例模式。"),
    
    ("Spring AOP 是什么？实现原理？", "中级", ["Spring", "AOP"],
     "AOP（面向切面编程）将横切关注点（日志、事务、安全）与业务逻辑分离。实现原理：1) JDK动态代理：基于接口的代理，通过InvocationHandler和Proxy实现。2) CGLIB代理：基于继承的代理，通过字节码增强生成子类。Spring默认使用JDK动态代理，目标类没实现接口时用CGLIB。AspectJ是编译期织入（性能更好）。"),
    
    ("Spring 中 Bean 的作用域？", "初级", ["Spring", "Bean"],
     "1) singleton：单例（默认），整个容器中只有一个实例。2) prototype：多例，每次获取创建新实例。3) request：每个HTTP请求一个实例（Web应用）。4) session：每个HTTP会话一个实例。5) application：ServletContext级别。6) websocket：WebSocket级别。注意：singleton Bean是线程不安全的，需自行处理并发问题。"),
    
    ("Spring 怎么解决循环依赖？", "高级", ["Spring", "循环依赖"],
     "Spring通过三级缓存解决单例Bean的循环依赖：1) 一级缓存（singletonObjects）：存放完全初始化好的Bean。2) 二级缓存（earlySingletonObjects）：存放早期暴露的Bean（尚未填充属性）。3) 三级缓存（singletonFactories）：存放Bean的工厂对象（ObjectFactory）。过程：A创建→提前暴露工厂到三级缓存→填充属性时发现依赖B→B创建时依赖A→从三级缓存获取A的早期引用→B完成→A完成。仅支持单例的setter注入循环依赖，构造器注入和prototype不支持。"),
    
    ("Spring 用到了哪些设计模式？", "中级", ["Spring", "设计模式"],
     "1) 工厂模式：BeanFactory/ApplicationContext。2) 单例模式：默认Bean作用域。3) 代理模式：AOP实现。4) 模板方法模式：JdbcTemplate/RestTemplate。5) 观察者模式：ApplicationEvent事件机制。6) 适配器模式：HandlerAdapter。7) 装饰器模式：BeanWrapper。8) 策略模式：Resource不同实现。"),
    
    ("Spring 事务在哪些场景下会失效？", "高级", ["Spring", "事务"],
     "1) 方法非public（CGLIB代理需要public）。2) 同类方法调用（this.method()不经过代理）。3) 异常被catch未抛出（事务只回滚RuntimeException和Error）。4) rollbackFor设置不匹配（默认不回滚受检异常）。5) 数据库引擎不支持事务（MyISAM）。6) 多线程环境（事务绑定线程，新线程无事务）。7) propagation设置不当（如PROPAGATION_NOT_SUPPORTED）。"),
    
    ("@Autowired 和 @Resource 的区别？", "初级", ["Spring", "注解"],
     "@Autowired：Spring提供，默认按类型（byType）注入，配合@Qualifier可按名称注入。@Resource：JDK提供（JSR-250），默认按名称（byName）注入，找不到再按类型。@Autowired通过AutowiredAnnotationBeanPostProcessor处理，可配合required=false可选注入。"),
    
    ("SpringMVC 的执行流程？", "中级", ["SpringMVC"],
     "1) 请求到达DispatcherServlet（前端控制器）。2) DispatcherServlet调用HandlerMapping找到对应的Handler（处理器映射器）。3) 通过HandlerAdapter调用具体的Controller（处理器适配器）。4) Controller执行业务逻辑，返回ModelAndView。5) ViewResolver解析视图名称（视图解析器）。6) View渲染数据生成响应。7) 返回响应给客户端。"),
    
    ("拦截器和过滤器的区别？", "中级", ["SpringMVC", "Servlet"],
     "1) 过滤器（Filter）：Servlet规范的一部分，基于函数回调，可拦截所有请求（包括静态资源），在请求进入Servlet前和响应返回前执行。2) 拦截器（Interceptor）：Spring MVC框架组件，基于Java反射机制（AOP），只拦截Controller请求，可访问Spring上下文（获取Bean）。执行顺序：Filter → Interceptor → Controller。"),
    
    ("SpringBoot 自动配置原理？", "高级", ["SpringBoot", "自动配置"],
     "核心是@SpringBootApplication注解，它包含@EnableAutoConfiguration。流程：1) @EnableAutoConfiguration通过@Import导入AutoConfigurationImportSelector。2) 读取META-INF/spring.factories中的自动配置类全限定名。3) 根据@Conditional条件注解（@ConditionalOnClass/@ConditionalOnBean/@ConditionalOnProperty等）过滤。4) 满足条件的配置类生效，自动注入所需Bean。开发时可通过exclude排除不需要的自动配置。"),
    
    ("MyBatis 中 #{} 和 ${} 的区别？", "初级", ["MyBatis", "SQL注入"],
     "#{}：预编译占位符，将参数作为字符串处理，自动加引号，防止SQL注入，推荐使用。${}：字符串替换，直接拼接SQL，存在SQL注入风险。使用场景：#{}用于普通值（WHERE name = #{name}），${}用于动态表名/列名/ORDER BY（ORDER BY ${column}）。"),
    
    ("MyBatis 缓存机制？", "中级", ["MyBatis", "缓存"],
     "一级缓存（SqlSession级别）：默认开启，同一个SqlSession中相同查询会从缓存获取，SqlSession关闭时清空。二级缓存（Mapper级别）：跨SqlSession共享，需手动开启（mapper.xml中<cache/>），多个SqlSession可共享。注意事项：缓存可能造成脏读（另一个进程修改了数据），分布式环境需使用Redis等外部缓存替代。"),
]

for title, diff, tags, answer in spring:
    questions.append(add_q("后端开发", diff, title, answer, tags))

# ==== SECTION 7: 微服务 & 分布式 ====
micro = [
    ("什么是服务熔断？什么是服务降级？", "中级", ["微服务", "容错"],
     "服务熔断：当某个服务调用失败达到阈值时，自动切断对该服务的调用（熔断器打开状态），防止级联故障（雪崩效应）。一段时间后进入半开状态尝试调用，成功则关闭熔断器。服务降级：在系统压力过大或部分服务不可用时，返回一个托底方案（默认值、缓存数据、友好提示），保证核心业务可用。熔断是降级的一种方式。常用组件：Sentinel、Hystrix、Resilience4j。"),
    
    ("Nacos 和 Eureka 的区别？", "中级", ["微服务", "注册中心"],
     "1) CAP：Eureka是AP（可用性+分区容错，牺牲一致性）；Nacos支持AP和CP模式切换。2) 健康检查：Eureka通过心跳保护机制（自我保护模式）；Nacos支持临时实例（心跳）和持久实例（主动探测）。3) 功能：Nacos集成了配置中心功能，Eureka需要配合Spring Cloud Config。4) Nacos使用Raft协议保证CP，适合对一致性要求高的场景。5) Nacos支持DNS-based服务发现，跨语言场景更友好。"),
    
    ("网关的作用是什么？Gateway 和 Zuul 的区别？", "中级", ["微服务", "网关"],
     "网关作用：1) 路由转发。2) 统一鉴权认证。3) 限流熔断。4) 日志监控。5) 跨域处理。6) 协议转换。Gateway vs Zuul：Gateway基于Spring 5 WebFlux（Reactor-netty），非阻塞异步，性能优于Zuul 1.x（基于Servlet阻塞IO）。Gateway支持Predicate断言和Filter过滤器灵活路由规则。生产环境推荐Gateway。"),
    
    ("Feign 和 OpenFeign 的区别？", "初级", ["微服务", "RPC"],
     "Feign是Netflix开源的声明式HTTP客户端。OpenFeign是Spring Cloud对Feign的增强：1) 支持Spring MVC注解（@RequestMapping等）。2) 集成Ribbon实现负载均衡。3) 集成Hystrix/Sentinel实现熔断降级。4) 支持请求/响应拦截器和编码器自定义。使用：定义接口+注解，自动生成HTTP调用实现。"),
    
    ("消息队列有什么作用？为什么使用MQ？", "中级", ["消息队列", "MQ"],
     "作用：1) 异步处理：耗时操作异步执行，提高响应速度。2) 应用解耦：系统间通过消息通信，不直接依赖。3) 流量削峰：高峰期请求先入队列，平滑后端处理压力。4) 数据分发：一对多广播。5) 最终一致性：分布式事务的解决方案之一。常见MQ：RabbitMQ（稳定性高）、RocketMQ（事务消息强）、Kafka（高吞吐，大数据场景）。"),
    
    ("如何保证消息不丢失？", "高级", ["消息队列", "可靠性"],
     "需在生产、MQ服务端、消费三阶段保障：1) 生产端：使用确认机制（publisher confirm），失败重试。2) MQ服务端：持久化消息到磁盘，集群部署+镜像队列（RabbitMQ）/副本机制（Kafka）。3) 消费端：手动ACK确认，消费成功后再确认。RabbitMQ：消息persistent+queue durable+手动ack。Kafka：设置acks=all，min.insync.replicas>=2，enable.idempotence=true。"),
    
    ("分布式事务的解决方案？", "高级", ["分布式", "事务"],
     "两大类：1) 强一致性方案：两阶段提交（2PC）/三阶段提交（3PC），基于XA协议，但性能较差。2) 最终一致性方案（主流）：TCC模式（Try-Confirm-Cancel，需业务代码实现）；基于消息队列的最终一致性（RocketMQ事务消息）；本地消息表（本地操作+消息表同事务，定时重试）；Saga模式（长事务拆分为本地事务链+补偿）。推荐使用Seata框架，支持AT/TCC/Saga/XA四种模式，AT模式对业务无侵入。"),
    
    ("分布式锁的实现方式？", "高级", ["分布式", "锁"],
     "1) 数据库：InnoDB行级锁（SELECT...FOR UPDATE），性能差。2) Redis：SET NX EX（原子加锁+设置过期时间），Redisson提供看门狗自动续期+可重入锁。3) Zookeeper：临时顺序节点+Watch机制，公平锁，强一致性。推荐：Redis用于性能要求高的场景，Zookeeper用于强一致性场景。分布式锁要点：互斥性、防死锁（过期时间）、容错性、加锁解锁原子性。"),
    
    ("分布式 Session 解决方案？", "中级", ["分布式", "Session"],
     "1) Session复制：Tomcat自带，每个节点同步Session，浪费带宽。2) Session黏性（Sticky）：Nginx ip_hash，同一IP请求固定到一台服务器，但服务器宕机会丢失。3) 集中式Session存储（推荐）：Redis存储Session，Spring Session框架自动管理，各服务统一读写。4) JWT：无状态方案，将用户信息加密到Token中，服务端不需存储Session。"),
    
    ("CAP 理论和 BASE 理论？", "高级", ["分布式", "理论"],
     "CAP理论：分布式系统最多同时满足一致性(C)、可用性(A)、分区容错性(P)中的两个。P是必须的（网络分区不可避免），因此通常在CP（强一致性，如Zookeeper/Nacos CP）和AP（高可用，如Eureka/Nacos AP）之间权衡。BASE理论：对CAP中AP方案的延伸，Basically Available（基本可用）、Soft state（软状态）、Eventually consistent（最终一致性）。核心思想：不追求强一致性，允许系统存在中间状态，最终达到一致。"),
]

for title, diff, tags, answer in micro:
    questions.append(add_q("后端开发", diff, title, answer, tags))

# ==== SECTION 8: Redis ====
redis_q = [
    ("Redis 的数据类型及使用场景？", "中级", ["Redis", "数据类型"],
     "1) String：缓存对象、计数器、分布式锁、Session共享（最常用）。2) Hash：存储对象属性（如用户信息），方便部分字段更新。3) List：消息队列、最新列表（LPUSH+LRANGE实现分页）。4) Set：去重、共同好友（交集）、抽奖。5) ZSet（Sorted Set）：排行榜、延迟队列、带权重的集合。6) Bitmap：签到统计、布隆过滤器。7) HyperLogLog：UV统计（非精确去重）。8) Geo：地理位置（附近的人）。"),
    
    ("Redis 为什么快？", "中级", ["Redis", "性能"],
     "1) 纯内存操作，读写速度极快（微秒级）。2) 单线程模型，避免多线程上下文切换和锁竞争。3) IO多路复用（epoll），一个线程同时监听多个Socket连接。4) 高效的数据结构（SDS、ziplist、skipList等）。5) RESP协议简单高效，解析开销小。注意：Redis 6.0+引入多线程处理网络IO，但命令执行仍是单线程。"),
    
    ("Redis 的持久化机制？", "中级", ["Redis", "持久化"],
     "RDB（快照）：定时将内存数据保存到dump.rdb文件。优点：文件紧凑、恢复快、适合冷备份。缺点：可能丢失最后一次快照后的数据。AOF（追加日志）：记录每个写命令到appendonly.aof文件。优点：数据安全性高（最多丢失1秒）、日志可读。缺点：文件大、恢复慢。AOF重写可压缩日志。推荐：同时开启RDB和AOF，AOF保证数据安全，RDB做冷备份备份。"),
    
    ("缓存穿透、缓存击穿、缓存雪崩？", "高级", ["Redis", "缓存问题"],
     "缓存穿透：查询不存在的数据，请求直接打到数据库。解决：布隆过滤器、缓存空值（设短过期时间）、参数校验。缓存击穿：热点key过期瞬间大量请求打到数据库。解决：互斥锁（只让一个线程查DB并回写缓存）、永不过期（逻辑过期异步更新）。缓存雪崩：大量key同时过期或Redis宕机，请求全部打到数据库。解决：key过期时间加随机值、高可用（主从+哨兵/集群）、限流降级、多级缓存。"),
    
    ("缓存与数据库双写一致性？", "高级", ["Redis", "一致性"],
     "方案：1) 先更新数据库，再删除缓存（Cache Aside Pattern，推荐）。2) 延迟双删：删除缓存→更新DB→延迟再删一次。3) Canal + MQ异步更新：监听MySQL binlog，通过MQ通知更新缓存，业务无侵入。4) 对一致性要求不高：设置过期时间兜底。5) 强一致性：分布式读写锁（Redisson RReadWriteLock）。读多写少用旁路缓存+延迟双删，写高频用异步回写，强一致用分布式锁+直写。"),
    
    ("Redis 过期策略和内存淘汰策略？", "中级", ["Redis", "策略"],
     "过期策略：定期删除（定时抽样删除过期key）+惰性删除（访问时检查是否过期）。内存淘汰策略（8种）：noeviction（默认，内存满报错）；allkeys-lru（最近最少使用）；allkeys-lfu（最不经常使用）；allkeys-random（随机）；volatile-lru（有过期时间的最近最少用）；volatile-lfu；volatile-random；volatile-ttl（即将过期优先）。推荐allkeys-lru保障热点数据。"),
    
    ("Redis 主从同步原理？", "中级", ["Redis", "主从"],
     "全量复制：从库发送PSYNC命令→主库执行BGSAVE生成RDB快照→发送RDB给从库→从库加载RDB→主库将缓冲区中的增量命令发送给从库执行。增量复制：主从断开重连后，主库根据replication offset只发送断开期间的命令。Redis 2.8+支持部分同步（PSYNC），使用runid+offset定位断点。注意：主从异步复制，可能短暂不一致。"),
    
    ("Redis 哨兵机制和集群模式？", "高级", ["Redis", "高可用"],
     "哨兵（Sentinel）：自动监控主从节点状态，主节点故障时自动选举新主并通知客户端。流程：主观下线（单个哨兵判断）→客观下线（多数哨兵确认）→选举Leader哨兵→选择新主（排除响应差、偏移量小的从节点）→执行failover→通知客户端。集群（Cluster）：数据分片到16384个slot，每个节点负责部分slot，无中心节点。支持水平扩展、故障自动转移。槽位计算：CRC16(key) % 16384。"),
    
    ("Redis 实现分布式锁的原理？", "高级", ["Redis", "分布式锁"],
     "基本原理：SET key value NX EX seconds（原子操作）。需考虑：1) 锁过期时间：不能太短（业务执行完前过期）也不能太长（宕机后锁不释放）。2) 锁误删：value设唯一标识（UUID），释放时先get再del（Lua脚本保证原子性）。3) 可重入：Redisson通过hash记录重入次数。Redisson看门狗（Watch Dog）：自动续期，默认每10秒检查，续期到30秒，避免业务未完成锁过期。生产级推荐使用Redisson。"),
]

for title, diff, tags, answer in redis_q:
    questions.append(add_q("后端开发", diff, title, answer, tags))

# ==== SECTION 9: 其他（Dubbo/ZK/ES/Docker/SSO等） ====
other = [
    ("Dubbo 的工作流程？", "中级", ["Dubbo", "RPC"],
     "1) Provider向注册中心注册服务。2) Consumer向注册中心订阅服务，获取Provider地址列表并缓存到本地。3) Consumer通过RPC调用Provider（负载均衡选择节点）。4) Consumer和Provider异步通知监控中心（Monitor）。Dubbo底层使用Netty进行NIO异步通信，Hessian2进行二进制序列化。注册中心挂了不影响已有服务的调用（本地缓存）。"),
    
    ("Dubbo 负载均衡策略有哪些？", "中级", ["Dubbo", "负载均衡"],
     "1) Random LoadBalance：按权重随机（默认），可设置不同实例权重。2) RoundRobin LoadBalance：按权重轮询。3) LeastActive LoadBalance：最少活跃调用数，性能差的机器收到更少请求。4) ConsistentHash LoadBalance：一致性哈希，相同参数的请求总发到同一Provider。适用于订单等需同一机器处理的场景。"),
    
    ("Zookeeper 的功能有哪些？", "中级", ["Zookeeper", "分布式协调"],
     "1) 集群管理：监控节点存活状态。2) 主节点选举：Leader选举（ZAB协议）。3) 分布式锁：独占锁（临时节点）、共享锁。4) 命名服务：分布式系统中按名字获取资源地址。5) 配置管理：统一配置下发。6) Watch机制：节点变化时通知客户端。Zookeeper基于CP原则，保证强一致性。"),
    
    ("Elasticsearch 的核心概念？索引文档过程？", "中级", ["ES", "搜索引擎"],
     "核心概念：索引（Index）≈数据库，类型（Type）≈表（7.x废弃），文档（Document）≈行，分片（Shard）+副本（Replica）保证高可用。索引过程：协调节点计算分片（hash(document_id) % num_shards）→写入Memory Buffer→每秒refresh到Filesystem Cache（可搜索）→translog保证可靠性→定时flush到磁盘。删除/更新：标记.del文件，段合并时真正删除。"),
    
    ("Linux 常用命令有哪些？", "初级", ["Linux", "命令"],
     "ps -ef | grep java（查看Java进程）；tail -f xx.log（动态查看日志）；netstat -anp | grep 端口（查看端口占用）；nohup java -jar app.jar &（后台启动）；kill PID（终止进程）；find /path -name '*.txt'（查找文件）；df -h（磁盘空间）、free -m（内存）；top（实时进程监控）；chmod（权限修改）。"),
    
    ("Docker 的核心概念？", "初级", ["Docker", "容器"],
     "镜像（Image）：应用的打包模板（Dockerfile构建）。容器（Container）：镜像的运行实例（docker run）。仓库（Registry）：存储和分发镜像（docker push/pull）。数据卷（Volume）：容器和宿主机数据共享和持久化。Docker Compose：多容器编排（docker-compose.yml）。核心命令：docker images/ps/run/exec/logs/stop/rm。"),
    
    ("单点登录（SSO）和 OAuth 2.0 的区别？", "中级", ["SSO", "OAuth2"],
     "SSO（单点登录）：同一企业内多个应用共享登录状态，登录一次即可访问所有子系统。通过Cookie、JWT或CAS协议实现。OAuth 2.0（授权协议）：第三方应用获取用户资源授权，如微信登录。是授权协议，不是认证协议。OAuth 2.0四种授权模式：授权码模式（最安全）、密码模式、客户端模式、简化模式。"),
    
    ("如何设计一个 RESTful 接口？", "中级", ["API设计", "RESTful"],
     "接口四要素：请求路径（资源名词复数）、请求方式（GET查/POST增/PUT改/DELETE删）、入参（@RequestParam/@PathVariable/@RequestBody）、出参（统一返回格式{code, msg, data}）。路径规范：版本号（/api/v1/）、资源层级（/users/{id}/orders）。DTO用于入参，VO用于出参。注意幂等性（GET/PUT/DELETE幂等，POST不幂等）。"),
    
    ("定时任务框架对比：Quartz vs XXL-Job vs Spring Task？", "初级", ["定时任务", "调度"],
     "Spring Task：@Scheduled注解，单机简单任务，不支持分布式。Quartz：重量级，需持久化到数据库，系统侵入性高，不适用分布式场景。XXL-Job：轻量级分布式任务调度，支持集群、分片、失败重试、Cron表达式、路由策略（轮询/广播/分片）。推荐中小项目用XXL-Job（Web管理界面+邮件报警+弹性扩容）。"),
    
    ("RBAC 权限模型是什么？", "中级", ["权限", "RBAC"],
     "RBAC（基于角色的访问控制）：用户→角色→权限的三层模型。核心表设计（5张）：用户表、角色表、权限表、用户角色关系表、角色权限关系表。实现：Spring Security + Gateway网关拦截，通过权限值（如1=普通用户，2=VIP，4=管理员）做位运算判断。类似Linux的rwx权限管理。"),
]

for title, diff, tags, answer in other:
    questions.append(add_q("后端开发", diff, title, answer, tags))

# ==== 写入 JSON ====
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"提取完成：{len(questions)} 道后端面试题")
# 难度分布
from collections import Counter
diffs = Counter(q['difficulty'] for q in questions)
print(f"难度分布：{dict(diffs)}")

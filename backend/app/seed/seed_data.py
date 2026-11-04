"""
Seed data for InterviewPilot - comprehensive interview preparation content.
"""
from app.core.database import SessionLocal
from app.models.models import (
    Lesson, Quiz, SystemDesignProblem, CodingProblem, StarQuestion,
)


# ======================================================================
# LESSONS DATA
# ======================================================================

LESSONS = [
    # ========== JAVA (3 lessons) ==========
    {
        "category": "java",
        "title": "Collections Framework Deep Dive",
        "slug": "collections-framework-deep-dive",
        "difficulty": "advanced",
        "order_index": 1,
        "content": (
            "The Java Collections Framework is far more than a set of data structures; it is a carefully designed "
            "hierarchy of interfaces and implementations that every senior engineer must understand at a mechanical "
            "level. At its root sit the Iterable and Collection interfaces, branching into List, Set, Queue, and Deque. "
            "The Map hierarchy stands apart because a map is not conceptually a collection of elements but a collection "
            "of key-value pairs. Understanding where each interface sits in this hierarchy tells you which contracts "
            "an implementation must honor and which operations are optional.\n\n"

            "ArrayList and LinkedList both implement List, but their performance profiles differ dramatically. "
            "ArrayList uses a contiguous Object[] array that is resized by 50% when full (via Arrays.copyOf). Random "
            "access is O(1), but inserting or removing in the middle is O(n) because elements must shift. LinkedList "
            "is a doubly-linked node chain providing O(1) insertion and removal at known positions, but O(n) traversal "
            "to reach those positions. In practice, ArrayList almost always wins due to CPU cache locality: sequential "
            "reads from a contiguous array are dramatically faster on modern hardware than pointer-chasing through "
            "heap-allocated Node objects. LinkedList is a good choice only when you hold a ListIterator at the "
            "insertion point and never need random access.\n\n"

            "HashMap deserves special attention. Since Java 8, buckets that exceed a treeify threshold of 8 entries "
            "are converted from a linked list to a red-black tree, improving worst-case lookup from O(n) to O(log n). "
            "The load factor (default 0.75) controls when the internal table doubles in size. A resize rehashes every "
            "entry, so pre-sizing the map when the element count is known avoids repeated rehashing. "
            "ConcurrentHashMap uses a fundamentally different strategy: in Java 8+ it employs CAS operations on "
            "individual bins rather than segment-level locks, giving much better throughput under contention.\n\n"

            "TreeMap and TreeSet are backed by red-black trees and maintain elements in sorted order. NavigableMap "
            "methods like floorKey, ceilingKey, headMap, and tailMap make range queries efficient. LinkedHashMap "
            "preserves insertion order (or access order if constructed with accessOrder=true), which makes it a "
            "natural building block for an LRU cache: override removeEldestEntry to evict automatically.\n\n"

            "When choosing a collection, think about thread safety, null handling, ordering guarantees, and "
            "iteration stability. EnumSet and EnumMap are specialized for enum keys and are faster than their "
            "general-purpose counterparts. The Collections utility class provides unmodifiable wrappers, synchronized "
            "wrappers, and checked wrappers that enforce type safety at runtime. In Java 9+, List.of(), Set.of(), and "
            "Map.of() create truly immutable collections that reject null elements and throw on mutation."
        ),
        "examples": [
            {
                "title": "Pre-sizing HashMap to avoid rehashing",
                "code": (
                    "// If you know you will store 1000 entries, pre-size:\n"
                    "// capacity = (int)(expectedSize / loadFactor) + 1\n"
                    "Map<String, User> map = new HashMap<>(1334);\n"
                    "// Or since Java 19:\n"
                    "Map<String, User> map = HashMap.newHashMap(1000);"
                ),
            },
            {
                "title": "LRU Cache with LinkedHashMap",
                "code": (
                    "public class LRUCache<K, V> extends LinkedHashMap<K, V> {\n"
                    "    private final int maxSize;\n"
                    "    public LRUCache(int maxSize) {\n"
                    "        super(maxSize, 0.75f, true); // accessOrder = true\n"
                    "        this.maxSize = maxSize;\n"
                    "    }\n"
                    "    @Override\n"
                    "    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {\n"
                    "        return size() > maxSize;\n"
                    "    }\n"
                    "}"
                ),
            },
            {
                "title": "NavigableMap range queries",
                "code": (
                    "TreeMap<LocalDate, BigDecimal> prices = new TreeMap<>();\n"
                    "// Get all prices in Q1 2024\n"
                    "SortedMap<LocalDate, BigDecimal> q1 = prices.subMap(\n"
                    "    LocalDate.of(2024, 1, 1),\n"
                    "    LocalDate.of(2024, 4, 1)\n"
                    ");"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Explain why ConcurrentHashMap does not allow null keys or values, while HashMap does.",
                "hint": "Think about ambiguity: in a concurrent map, can you distinguish 'key maps to null' from 'key is absent' without a race condition?",
            },
            {
                "question": "You need a thread-safe Set that maintains insertion order. How would you build one?",
                "hint": "Consider Collections.newSetFromMap with a ConcurrentHashMap variant, or wrapping a LinkedHashSet.",
            },
        ],
        "tags": ["java", "collections", "hashmap", "data-structures", "performance"],
    },
    {
        "category": "java",
        "title": "Concurrency - Thread Safety, Locks, and Executors",
        "slug": "concurrency-thread-safety-locks-executors",
        "difficulty": "advanced",
        "order_index": 2,
        "content": (
            "Java concurrency is one of the most complex and interview-critical topics for senior engineers. "
            "At its core, the Java Memory Model (JMM) defines how threads interact through memory: every thread "
            "has a working memory (CPU cache) and the JMM specifies when writes become visible to other threads. "
            "The happens-before relationship is the formal guarantee: if action A happens-before action B, then "
            "the effects of A are visible to B. Key happens-before edges include: monitor unlock to subsequent lock, "
            "volatile write to subsequent read, thread start to the started thread's first action, and thread "
            "termination (join) to the joining thread's subsequent actions.\n\n"

            "The synchronized keyword provides mutual exclusion and memory visibility. Every synchronized block "
            "acquires a monitor lock on entry and releases it on exit, establishing a happens-before edge. "
            "The volatile keyword guarantees visibility without mutual exclusion: a volatile write flushes the "
            "writing thread's cache, and a volatile read invalidates the reading thread's cache for that variable. "
            "Volatile is sufficient for flags and single-variable state, but compound operations (check-then-act, "
            "read-modify-write) still need synchronization or atomic classes.\n\n"

            "The java.util.concurrent.locks package provides ReentrantLock, which adds tryLock (with timeout), "
            "interruptible locking, and fairness ordering that synchronized cannot offer. ReadWriteLock allows "
            "concurrent reads but exclusive writes, improving throughput for read-heavy workloads. StampedLock "
            "(Java 8+) adds optimistic reads: you acquire a stamp, read shared state, then validate the stamp. "
            "If no write occurred, you proceed without blocking. If the stamp is invalid, you fall back to a "
            "pessimistic read lock. This can dramatically reduce contention in hot read paths.\n\n"

            "The Executor framework decouples task submission from execution policy. ThreadPoolExecutor is the "
            "workhorse: corePoolSize threads are kept alive, up to maximumPoolSize threads are created under load, "
            "and a BlockingQueue buffers tasks in between. The rejection policy (AbortPolicy, CallerRunsPolicy, "
            "DiscardPolicy, DiscardOldestPolicy) governs what happens when both the pool and queue are full. "
            "ForkJoinPool (used by parallel streams) implements work-stealing: idle threads steal tasks from busy "
            "threads' deques, achieving good load balancing for recursive divide-and-conquer workloads.\n\n"

            "CompletableFuture chains asynchronous computations without blocking threads. Methods like thenApply, "
            "thenCompose, thenCombine, and exceptionally form a DAG of dependent stages. Virtual threads (Java 21, "
            "Project Loom) are lightweight threads managed by the JVM rather than the OS: they make the thread-per-"
            "request model viable at scale by allowing millions of concurrent threads with minimal memory overhead. "
            "Virtual threads automatically unmount from carrier threads when blocking on I/O, freeing the carrier "
            "for other virtual threads."
        ),
        "examples": [
            {
                "title": "StampedLock optimistic read pattern",
                "code": (
                    "private final StampedLock lock = new StampedLock();\n"
                    "private double x, y;\n\n"
                    "public double distanceFromOrigin() {\n"
                    "    long stamp = lock.tryOptimisticRead();\n"
                    "    double currentX = x, currentY = y;\n"
                    "    if (!lock.validate(stamp)) {\n"
                    "        stamp = lock.readLock();\n"
                    "        try { currentX = x; currentY = y; }\n"
                    "        finally { lock.unlockRead(stamp); }\n"
                    "    }\n"
                    "    return Math.sqrt(currentX * currentX + currentY * currentY);\n"
                    "}"
                ),
            },
            {
                "title": "Configuring ThreadPoolExecutor",
                "code": (
                    "ExecutorService pool = new ThreadPoolExecutor(\n"
                    "    4,                          // corePoolSize\n"
                    "    16,                         // maximumPoolSize\n"
                    "    60L, TimeUnit.SECONDS,      // keepAliveTime\n"
                    "    new LinkedBlockingQueue<>(1000), // bounded queue\n"
                    "    new ThreadPoolExecutor.CallerRunsPolicy()\n"
                    ");"
                ),
            },
            {
                "title": "CompletableFuture composition",
                "code": (
                    "CompletableFuture<Order> orderFuture = CompletableFuture\n"
                    "    .supplyAsync(() -> fetchUser(userId))\n"
                    "    .thenCompose(user -> fetchCart(user.getId()))\n"
                    "    .thenCombine(\n"
                    "        CompletableFuture.supplyAsync(() -> fetchInventory()),\n"
                    "        (cart, inventory) -> createOrder(cart, inventory)\n"
                    "    )\n"
                    "    .exceptionally(ex -> {\n"
                    "        log.error(\"Order failed\", ex);\n"
                    "        return Order.failed(ex.getMessage());\n"
                    "    });"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Design a thread-safe bounded buffer using ReentrantLock and Condition variables. Support put() that blocks when full and take() that blocks when empty.",
                "hint": "Use two Condition objects: notFull and notEmpty. Signal the opposite condition after each operation.",
            },
            {
                "question": "Explain why double-checked locking without volatile is broken in Java. What does volatile add?",
                "hint": "Without volatile, the JMM allows reordering of object construction: another thread can see a non-null reference to a partially constructed object.",
            },
        ],
        "tags": ["java", "concurrency", "threads", "locks", "executor", "completable-future"],
    },
    {
        "category": "java",
        "title": "JVM Internals - Memory Model and Garbage Collection",
        "slug": "jvm-internals-memory-model-garbage-collection",
        "difficulty": "advanced",
        "order_index": 3,
        "content": (
            "Understanding JVM internals is essential for diagnosing production issues and optimizing application "
            "performance. The JVM divides memory into several runtime data areas. The heap stores all object "
            "instances and arrays, shared among all threads. The metaspace (replacing PermGen since Java 8) stores "
            "class metadata, method bytecode, and the constant pool. Each thread gets its own stack (default 512KB "
            "to 1MB) holding stack frames with local variables and operand stacks. The program counter register "
            "tracks the currently executing bytecode instruction per thread.\n\n"

            "The generational hypothesis - most objects die young - drives the design of generational garbage "
            "collectors. The heap is divided into Young Generation (Eden + two Survivor spaces) and Old Generation. "
            "New objects are allocated in Eden. When Eden fills, a minor GC (young collection) copies live objects "
            "to a Survivor space and increments their age. Objects surviving enough minor GCs (default threshold 15) "
            "are tenured (promoted) to Old Gen. Major GC collects Old Gen and is typically much more expensive. "
            "Large objects that exceed a threshold bypass Eden entirely and are allocated directly in Old Gen.\n\n"

            "Modern collectors include G1 (default since Java 9), ZGC, and Shenandoah. G1 divides the heap into "
            "equally-sized regions (1-32MB each) and tracks the amount of garbage in each. During a mixed GC, G1 "
            "collects the regions with the most garbage first (hence Garbage-First). G1 aims to meet a target pause "
            "time (default 200ms via -XX:MaxGCPauseMillis). ZGC (production-ready since Java 15) achieves sub-"
            "millisecond pause times regardless of heap size by using colored pointers and load barriers to perform "
            "relocation concurrently. ZGC handles heaps from 8MB to 16TB with pauses typically under 1ms.\n\n"

            "Key JVM tuning flags include: -Xms and -Xmx for initial and max heap size, -XX:NewRatio for young-to-"
            "old generation ratio, -XX:MetaspaceSize for initial metaspace, -XX:+UseG1GC or -XX:+UseZGC to select "
            "the collector. Diagnostic flags like -XX:+PrintGCDetails, -Xlog:gc* (Java 9+), and -XX:+HeapDumpOn"
            "OutOfMemoryError are invaluable in production. Tools like jstat, jmap, jcmd, and async-profiler help "
            "diagnose memory leaks, GC pressure, and allocation hotspots.\n\n"

            "Common memory issues include: memory leaks from unclosed resources or static collections that grow "
            "unboundedly, metaspace leaks from classloader churn in application servers, direct memory (off-heap) "
            "exhaustion from NIO ByteBuffers, and premature promotion causing Old Gen churn. Understanding the "
            "GC logs - identifying full GC frequency, pause durations, promotion rates, and allocation rates - is "
            "the single most important diagnostic skill for JVM performance work."
        ),
        "examples": [
            {
                "title": "Reading GC logs with unified logging (Java 9+)",
                "code": (
                    "# Enable unified GC logging\n"
                    "java -Xlog:gc*:file=gc.log:time,uptime,level,tags \\\n"
                    "     -XX:+UseG1GC \\\n"
                    "     -XX:MaxGCPauseMillis=100 \\\n"
                    "     -Xms4g -Xmx4g \\\n"
                    "     -jar myapp.jar\n\n"
                    "# Key log entries to watch:\n"
                    "# [gc] GC(42) Pause Young (Normal) 3200M->1200M(4096M) 15.3ms\n"
                    "# [gc] GC(43) Pause Full (Allocation Failure) 3900M->800M(4096M) 1200ms"
                ),
            },
            {
                "title": "Diagnosing a memory leak with jcmd",
                "code": (
                    "# Take a heap histogram (no full GC triggered)\n"
                    "jcmd <pid> GC.class_histogram | head -30\n\n"
                    "# Dump heap for analysis in Eclipse MAT or VisualVM\n"
                    "jcmd <pid> GC.heap_dump /tmp/heapdump.hprof\n\n"
                    "# Check native memory tracking\n"
                    "# Start JVM with: -XX:NativeMemoryTracking=summary\n"
                    "jcmd <pid> VM.native_memory summary"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Your application has frequent Full GC pauses of 2-3 seconds. GC logs show Old Gen is nearly full before each Full GC. What are the likely causes and how would you diagnose?",
                "hint": "Consider: heap too small, memory leak, premature promotion. Use heap dumps to find the largest retained objects.",
            },
            {
                "question": "Explain the trade-off between G1 and ZGC. When would you choose each?",
                "hint": "G1 has good throughput but pauses scale with heap and live set. ZGC has near-zero pauses but slightly lower throughput due to load barriers.",
            },
        ],
        "tags": ["java", "jvm", "garbage-collection", "memory", "performance", "tuning"],
    },

    # ========== SPRING BOOT (3 lessons) ==========
    {
        "category": "spring_boot",
        "title": "Dependency Injection and Inversion of Control",
        "slug": "dependency-injection-inversion-of-control",
        "difficulty": "intermediate",
        "order_index": 1,
        "content": (
            "Dependency Injection (DI) is the mechanism by which Spring achieves Inversion of Control (IoC). "
            "Instead of a class creating its own dependencies via the new keyword, the container injects them at "
            "construction time or through setter methods. This decouples components, makes unit testing trivial "
            "(inject mocks instead of real implementations), and centralizes configuration. The Spring IoC "
            "container - represented by ApplicationContext - manages the full lifecycle of beans: instantiation, "
            "dependency resolution, initialization callbacks, and destruction.\n\n"

            "Spring supports three injection styles: constructor injection, setter injection, and field injection "
            "(via @Autowired on fields). Constructor injection is strongly preferred because it makes dependencies "
            "explicit, enforces immutability via final fields, and guarantees the object is fully initialized at "
            "construction. With constructor injection, Spring resolves the dependency graph at startup, failing fast "
            "if any circular dependency or missing bean is detected. Since Spring 4.3, if a class has a single "
            "constructor, the @Autowired annotation is optional.\n\n"

            "Bean scopes control the lifecycle and sharing of instances. Singleton (default) creates one instance "
            "per ApplicationContext - suited for stateless services. Prototype creates a new instance on every "
            "injection or getBean() call, but Spring does not manage the destruction lifecycle of prototype beans. "
            "Request and Session scopes create instances per HTTP request or session, requiring a web-aware context. "
            "A common pitfall is injecting a shorter-lived scope (e.g., request) into a longer-lived scope "
            "(e.g., singleton): Spring handles this via scoped proxies (proxyMode = ScopedProxyMode.TARGET_CLASS) "
            "that delegate to the correct instance per request.\n\n"

            "The @Configuration and @Bean annotations define beans programmatically. @Configuration classes are "
            "processed by CGLIB to ensure that @Bean methods called from other @Bean methods return the same "
            "singleton instance rather than creating a new one. This is called full mode. @Component classes "
            "with @Bean methods run in lite mode, where inter-method calls create new instances. Understanding "
            "this distinction prevents subtle bugs in production.\n\n"

            "Conditional bean registration via @Conditional, @ConditionalOnProperty, @ConditionalOnClass, and "
            "@Profile allows different beans to be active in different environments. Spring Boot auto-configuration "
            "leverages these annotations heavily: it inspects the classpath and existing beans to decide which "
            "configurations to apply. You can inspect which auto-configurations were matched or excluded using "
            "the --debug flag or the conditions endpoint in Actuator."
        ),
        "examples": [
            {
                "title": "Constructor injection with immutable dependencies",
                "code": (
                    "@Service\n"
                    "public class OrderService {\n"
                    "    private final UserRepository userRepository;\n"
                    "    private final PaymentGateway paymentGateway;\n"
                    "    private final EventPublisher eventPublisher;\n\n"
                    "    // No @Autowired needed with single constructor\n"
                    "    public OrderService(UserRepository userRepository,\n"
                    "                        PaymentGateway paymentGateway,\n"
                    "                        EventPublisher eventPublisher) {\n"
                    "        this.userRepository = userRepository;\n"
                    "        this.paymentGateway = paymentGateway;\n"
                    "        this.eventPublisher = eventPublisher;\n"
                    "    }\n"
                    "}"
                ),
            },
            {
                "title": "Conditional bean with @Profile",
                "code": (
                    "@Configuration\n"
                    "public class StorageConfig {\n"
                    "    @Bean\n"
                    "    @Profile(\"local\")\n"
                    "    public StorageService localStorage() {\n"
                    "        return new FileSystemStorageService(\"/tmp/uploads\");\n"
                    "    }\n\n"
                    "    @Bean\n"
                    "    @Profile(\"!local\")\n"
                    "    public StorageService s3Storage(AmazonS3 s3Client) {\n"
                    "        return new S3StorageService(s3Client, \"my-bucket\");\n"
                    "    }\n"
                    "}"
                ),
            },
        ],
        "exercises": [
            {
                "question": "You have a circular dependency between ServiceA and ServiceB. What strategies can you use to break it?",
                "hint": "Options: restructure to extract shared logic into a third service, use @Lazy on one injection point, use an event-based approach, or inject the ApplicationContext and look up lazily.",
            },
            {
                "question": "Explain why field injection (@Autowired on a private field) is discouraged. What problems does it create for testing?",
                "hint": "Field injection hides dependencies, prevents immutability, and forces tests to use reflection or Spring context rather than simple constructor calls.",
            },
        ],
        "tags": ["spring", "dependency-injection", "ioc", "beans", "configuration"],
    },
    {
        "category": "spring_boot",
        "title": "Aspect-Oriented Programming and Proxies",
        "slug": "aspect-oriented-programming-proxies",
        "difficulty": "advanced",
        "order_index": 2,
        "content": (
            "Aspect-Oriented Programming (AOP) in Spring addresses cross-cutting concerns - functionality that "
            "spans multiple classes and cannot be cleanly modularized with OOP alone. Logging, security, "
            "transaction management, caching, and metrics collection are classic cross-cutting concerns. Without "
            "AOP, you would scatter the same boilerplate across dozens of methods. With AOP, you define the logic "
            "once in an aspect and declare where it applies via pointcut expressions.\n\n"

            "Spring AOP uses runtime proxies, not bytecode weaving like AspectJ. For beans that implement at least "
            "one interface, Spring creates a JDK dynamic proxy (java.lang.reflect.Proxy) that implements the same "
            "interfaces. For beans without interfaces, Spring uses CGLIB to generate a subclass at runtime. "
            "Since Spring Boot 2.0, CGLIB proxies are the default even when interfaces are present, controlled by "
            "spring.aop.proxy-target-class=true. This has a critical implication: self-invocation (calling another "
            "method on the same bean via this.method()) bypasses the proxy, so any advice on the inner method will "
            "not execute. This is the single most common AOP pitfall.\n\n"

            "Pointcut expressions define where advice applies. The execution() designator matches method signatures: "
            "execution(* com.example.service.*.*(..)) matches any method in any class in the service package. "
            "The @annotation() designator matches methods bearing a specific annotation - this is how Spring's "
            "@Transactional, @Cacheable, and @Async work internally. You can compose pointcuts with &&, ||, and ! "
            "operators. The within() designator restricts by class type, and args() matches by argument types.\n\n"

            "Advice types are: @Before (runs before the method), @After (runs after, regardless of outcome), "
            "@AfterReturning (runs after successful return, can access the return value), @AfterThrowing (runs "
            "after an exception, can access the exception), and @Around (wraps the method entirely, controlling "
            "whether and how ProceedingJoinPoint.proceed() is called). @Around is the most powerful and is what "
            "Spring uses internally for @Transactional. It can modify arguments, suppress exceptions, change the "
            "return value, or skip the method entirely.\n\n"

            "Understanding proxy mechanics is vital for debugging. @Transactional on a private method does nothing "
            "because CGLIB cannot override private methods. @Transactional on a method called from within the same "
            "class does nothing because the call goes through this, not the proxy. To work around self-invocation, "
            "you can inject the bean into itself (lazy self-injection), extract the method to a separate bean, or "
            "use AspectJ compile-time weaving. In tests, you can verify proxy behavior by checking whether "
            "AopUtils.isAopProxy(bean) returns true."
        ),
        "examples": [
            {
                "title": "Custom timing aspect with @Around",
                "code": (
                    "@Aspect\n"
                    "@Component\n"
                    "public class TimingAspect {\n"
                    "    private static final Logger LOG = LoggerFactory.getLogger(TimingAspect.class);\n\n"
                    "    @Around(\"@annotation(Timed)\")\n"
                    "    public Object timeMethod(ProceedingJoinPoint pjp) throws Throwable {\n"
                    "        long start = System.nanoTime();\n"
                    "        try {\n"
                    "            return pjp.proceed();\n"
                    "        } finally {\n"
                    "            long elapsed = (System.nanoTime() - start) / 1_000_000;\n"
                    "            LOG.info(\"{}.{} took {}ms\",\n"
                    "                pjp.getTarget().getClass().getSimpleName(),\n"
                    "                pjp.getSignature().getName(), elapsed);\n"
                    "        }\n"
                    "    }\n"
                    "}"
                ),
            },
            {
                "title": "Self-invocation pitfall demonstration",
                "code": (
                    "@Service\n"
                    "public class PaymentService {\n"
                    "    @Transactional\n"
                    "    public void processPayment(Order order) {\n"
                    "        // This call bypasses the proxy - @Transactional is ignored!\n"
                    "        this.logPayment(order);\n"
                    "    }\n\n"
                    "    @Transactional(propagation = Propagation.REQUIRES_NEW)\n"
                    "    public void logPayment(Order order) {\n"
                    "        // Intended to run in a new transaction, but it won't\n"
                    "        auditRepo.save(new AuditEntry(order));\n"
                    "    }\n"
                    "}"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Write an aspect that retries any method annotated with @Retryable up to 3 times on any RuntimeException, with exponential backoff.",
                "hint": "Use @Around advice with @annotation(Retryable). Loop up to 3 times, catching RuntimeException and sleeping 2^attempt * 100ms before retrying.",
            },
            {
                "question": "Explain why @Cacheable on a method called from within the same service class does not cache. How would you fix it?",
                "hint": "Same self-invocation issue as @Transactional. Fix by extracting the cached method into a separate @Service bean.",
            },
        ],
        "tags": ["spring", "aop", "proxy", "aspect", "cross-cutting-concerns"],
    },
    {
        "category": "spring_boot",
        "title": "Spring Security with JWT Authentication",
        "slug": "spring-security-jwt-authentication",
        "difficulty": "advanced",
        "order_index": 3,
        "content": (
            "Spring Security is a powerful and highly customizable framework for authentication and authorization. "
            "Its architecture is built on a chain of servlet filters (the SecurityFilterChain) that intercept "
            "every HTTP request. Each filter in the chain handles a specific security concern: CORS, CSRF, "
            "authentication, authorization, exception handling, and session management. Understanding this filter "
            "chain is critical for debugging security issues and customizing behavior.\n\n"

            "JWT (JSON Web Token) authentication is a stateless approach where the server does not store session "
            "state. After successful login, the server issues a signed JWT containing claims (user ID, roles, "
            "expiration). The client includes this token in the Authorization header as a Bearer token on every "
            "subsequent request. A custom filter (typically extending OncePerRequestFilter) extracts the token, "
            "validates the signature and expiration, parses the claims, and sets the SecurityContext with an "
            "authenticated UsernamePasswordAuthenticationToken.\n\n"

            "The SecurityFilterChain configuration in Spring Boot 3.x uses the lambda DSL with HttpSecurity. "
            "You disable CSRF for stateless APIs (since tokens are not vulnerable to CSRF), set session management "
            "to STATELESS, and define URL authorization rules with requestMatchers. The JWT filter is registered "
            "before UsernamePasswordAuthenticationFilter in the chain using addFilterBefore(). Password encoding "
            "uses BCryptPasswordEncoder (recommended) with its adaptive cost factor.\n\n"

            "Token refresh is essential for a production system. Short-lived access tokens (15-30 minutes) limit "
            "the damage window if a token is compromised. A longer-lived refresh token (days to weeks) is stored "
            "securely (HttpOnly cookie or secure storage) and used to obtain new access tokens. The refresh "
            "endpoint validates the refresh token, checks it has not been revoked, and issues a new access-refresh "
            "token pair. Token revocation can be implemented via a blocklist (Redis set of revoked JTI values) "
            "or by using short-lived tokens with a sliding window.\n\n"

            "Method-level security with @PreAuthorize and @PostAuthorize provides fine-grained access control. "
            "@PreAuthorize(\"hasRole('ADMIN')\") checks before method execution. @PreAuthorize(\"#userId == "
            "authentication.principal.id\") uses SpEL to compare method arguments with the authenticated user. "
            "@PostAuthorize(\"returnObject.owner == authentication.principal.username\") checks after execution "
            "and can filter the response. These annotations require @EnableMethodSecurity on a configuration class."
        ),
        "examples": [
            {
                "title": "JWT filter implementation",
                "code": (
                    "@Component\n"
                    "public class JwtAuthFilter extends OncePerRequestFilter {\n"
                    "    private final JwtService jwtService;\n"
                    "    private final UserDetailsService userDetailsService;\n\n"
                    "    @Override\n"
                    "    protected void doFilterInternal(HttpServletRequest req,\n"
                    "            HttpServletResponse res, FilterChain chain)\n"
                    "            throws ServletException, IOException {\n"
                    "        String header = req.getHeader(\"Authorization\");\n"
                    "        if (header == null || !header.startsWith(\"Bearer \")) {\n"
                    "            chain.doFilter(req, res);\n"
                    "            return;\n"
                    "        }\n"
                    "        String token = header.substring(7);\n"
                    "        String username = jwtService.extractUsername(token);\n"
                    "        if (username != null && SecurityContextHolder.getContext()\n"
                    "                .getAuthentication() == null) {\n"
                    "            UserDetails user = userDetailsService\n"
                    "                .loadUserByUsername(username);\n"
                    "            if (jwtService.isTokenValid(token, user)) {\n"
                    "                var auth = new UsernamePasswordAuthenticationToken(\n"
                    "                    user, null, user.getAuthorities());\n"
                    "                SecurityContextHolder.getContext()\n"
                    "                    .setAuthentication(auth);\n"
                    "            }\n"
                    "        }\n"
                    "        chain.doFilter(req, res);\n"
                    "    }\n"
                    "}"
                ),
            },
            {
                "title": "Security configuration with JWT",
                "code": (
                    "@Configuration\n"
                    "@EnableMethodSecurity\n"
                    "public class SecurityConfig {\n"
                    "    @Bean\n"
                    "    public SecurityFilterChain filterChain(HttpSecurity http,\n"
                    "            JwtAuthFilter jwtFilter) throws Exception {\n"
                    "        return http\n"
                    "            .csrf(csrf -> csrf.disable())\n"
                    "            .sessionManagement(sm -> sm\n"
                    "                .sessionCreationPolicy(SessionCreationPolicy.STATELESS))\n"
                    "            .authorizeHttpRequests(auth -> auth\n"
                    "                .requestMatchers(\"/api/auth/**\").permitAll()\n"
                    "                .requestMatchers(\"/api/admin/**\").hasRole(\"ADMIN\")\n"
                    "                .anyRequest().authenticated())\n"
                    "            .addFilterBefore(jwtFilter,\n"
                    "                UsernamePasswordAuthenticationFilter.class)\n"
                    "            .build();\n"
                    "    }\n"
                    "}"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Design a token refresh flow. What happens when the refresh token itself expires? How do you handle concurrent refresh requests?",
                "hint": "Consider refresh token rotation: each refresh returns a new refresh token and invalidates the old one. Use a mutex or one-time-use JTI to prevent race conditions.",
            },
            {
                "question": "How would you implement role-based and resource-based authorization in the same application?",
                "hint": "Use roles for coarse-grained access (admin, user) with hasRole() and resource ownership checks with SpEL expressions in @PreAuthorize referencing method parameters.",
            },
        ],
        "tags": ["spring-security", "jwt", "authentication", "authorization", "filter-chain"],
    },

    # ========== PYTHON (2 lessons) ==========
    {
        "category": "python",
        "title": "Decorators and Metaclasses",
        "slug": "decorators-and-metaclasses",
        "difficulty": "advanced",
        "order_index": 1,
        "content": (
            "Decorators are one of Python's most powerful features, enabling clean cross-cutting functionality "
            "without modifying the original function or class. A decorator is simply a callable that takes a "
            "callable and returns a callable. When you write @decorator above a function definition, Python "
            "executes function = decorator(function). Understanding this desugaring is key: decorators are "
            "not magic, they are higher-order functions. The functools.wraps decorator should always be applied "
            "to the inner wrapper function to preserve the original function's __name__, __doc__, and __module__.\n\n"

            "Decorators can be stacked (@d1 @d2 def f is equivalent to f = d1(d2(f))), and they can accept "
            "arguments. A decorator with arguments requires an extra level of nesting: the outermost function "
            "accepts the arguments and returns the actual decorator. Class-based decorators implement __call__ "
            "and can maintain state between invocations. This is useful for rate limiters, caches, and retry "
            "logic. The built-in functools.lru_cache and functools.cache decorators memoize function results, "
            "while functools.singledispatch enables function overloading based on the first argument's type.\n\n"

            "Class decorators modify or replace a class after it is defined. A class decorator receives the class "
            "object and returns a (possibly modified) class. dataclasses.dataclass is the most well-known class "
            "decorator: it inspects type annotations and generates __init__, __repr__, __eq__, and optionally "
            "__hash__ and comparison methods. You can write class decorators that add methods, register classes "
            "in a registry, or wrap all methods with logging.\n\n"

            "Metaclasses operate at a deeper level: they control how classes themselves are created. Every class "
            "in Python is an instance of its metaclass; the default metaclass is type. When you write "
            "class Foo(metaclass=MyMeta), Python calls MyMeta('Foo', bases, namespace) to create the class object. "
            "The __new__ method of the metaclass can inspect and modify the class namespace before the class is "
            "created, while __init_subclass__ (introduced in Python 3.6) provides a simpler hook that runs when "
            "a class is subclassed, without requiring a full metaclass.\n\n"

            "In practice, metaclasses are rarely needed in application code. They shine in framework design: "
            "Django's Model metaclass collects Field descriptors and builds the ORM mapping, SQLAlchemy's "
            "declarative base uses a metaclass to register table mappings, and ABC uses ABCMeta to enforce "
            "abstract method implementation. For most use cases, class decorators or __init_subclass__ are "
            "simpler and preferred. The rule of thumb: use decorators for cross-cutting behavior, "
            "__init_subclass__ for lightweight class registration or validation, and metaclasses only when "
            "you need to intercept class creation at the lowest level."
        ),
        "examples": [
            {
                "title": "Decorator with arguments and functools.wraps",
                "code": (
                    "import functools\n"
                    "import time\n\n"
                    "def retry(max_attempts=3, delay=1.0):\n"
                    "    def decorator(func):\n"
                    "        @functools.wraps(func)\n"
                    "        def wrapper(*args, **kwargs):\n"
                    "            last_exc = None\n"
                    "            for attempt in range(1, max_attempts + 1):\n"
                    "                try:\n"
                    "                    return func(*args, **kwargs)\n"
                    "                except Exception as e:\n"
                    "                    last_exc = e\n"
                    "                    if attempt < max_attempts:\n"
                    "                        time.sleep(delay * attempt)\n"
                    "            raise last_exc\n"
                    "        return wrapper\n"
                    "    return decorator\n\n"
                    "@retry(max_attempts=5, delay=0.5)\n"
                    "def fetch_data(url):\n"
                    "    return requests.get(url).json()"
                ),
            },
            {
                "title": "Plugin registry with __init_subclass__",
                "code": (
                    "class PluginBase:\n"
                    "    _registry = {}\n\n"
                    "    def __init_subclass__(cls, plugin_name=None, **kwargs):\n"
                    "        super().__init_subclass__(**kwargs)\n"
                    "        name = plugin_name or cls.__name__.lower()\n"
                    "        PluginBase._registry[name] = cls\n\n"
                    "    @classmethod\n"
                    "    def get_plugin(cls, name):\n"
                    "        return cls._registry[name]\n\n"
                    "class JsonParser(PluginBase, plugin_name='json'):\n"
                    "    def parse(self, data): ...\n\n"
                    "class XmlParser(PluginBase, plugin_name='xml'):\n"
                    "    def parse(self, data): ...\n\n"
                    "# PluginBase.get_plugin('json') -> JsonParser"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Write a @validate_types decorator that checks function argument types at runtime using the function's type annotations.",
                "hint": "Use inspect.signature to get parameters, match them with annotations, and check isinstance before calling the function.",
            },
            {
                "question": "Explain the difference between using a metaclass and __init_subclass__ for class registration. When would you need the metaclass approach?",
                "hint": "__init_subclass__ runs after the class is created. A metaclass's __new__ runs during creation and can modify the namespace before the class exists.",
            },
        ],
        "tags": ["python", "decorators", "metaclasses", "advanced-python", "design-patterns"],
    },
    {
        "category": "python",
        "title": "Async Programming with asyncio",
        "slug": "async-programming-asyncio",
        "difficulty": "advanced",
        "order_index": 2,
        "content": (
            "Asynchronous programming in Python centers on the asyncio library and the async/await syntax. "
            "Unlike threading, asyncio uses cooperative multitasking on a single thread: coroutines explicitly "
            "yield control at await points, and the event loop schedules the next ready coroutine. This avoids "
            "the overhead of thread context switching and eliminates most race conditions, since only one "
            "coroutine runs at a time between await points. However, any CPU-bound work between awaits blocks "
            "the entire event loop.\n\n"

            "A coroutine is defined with async def and returns a coroutine object when called (it does not execute "
            "immediately). To run it, you either await it (from inside another coroutine) or schedule it on the "
            "event loop with asyncio.create_task(). create_task returns a Task object that starts executing "
            "concurrently. asyncio.gather() runs multiple awaitables concurrently and returns their results in "
            "order. asyncio.wait() provides more control: you can wait for the first completed task "
            "(return_when=FIRST_COMPLETED) for patterns like racing or timeouts.\n\n"

            "asyncio.TaskGroup (Python 3.11+) is the modern structured concurrency primitive. It ensures that "
            "all tasks in the group complete or are cancelled if any task raises an exception. This prevents "
            "orphaned tasks that continue running in the background after an error. The async with pattern "
            "guarantees cleanup: async with asyncio.TaskGroup() as tg: tg.create_task(coro()) runs all tasks "
            "and propagates any exceptions as an ExceptionGroup.\n\n"

            "Synchronization primitives (asyncio.Lock, Semaphore, Event, Condition) mirror their threading "
            "counterparts but are designed for coroutines. An asyncio.Semaphore is commonly used to limit "
            "concurrent connections (e.g., at most 10 concurrent HTTP requests). asyncio.Queue provides a "
            "producer-consumer pattern for coroutines. For CPU-bound work, use loop.run_in_executor() to "
            "offload to a ThreadPoolExecutor or ProcessPoolExecutor without blocking the event loop.\n\n"

            "In production, aiohttp (or httpx with async) provides async HTTP clients, asyncpg provides async "
            "PostgreSQL access, and aiokafka provides async Kafka consumers. FastAPI is built on asyncio, so "
            "async def endpoints run on the event loop. Debugging async code requires understanding the event "
            "loop: asyncio.get_event_loop().set_debug(True) enables slow-callback warnings and provides better "
            "tracebacks. Common pitfalls include forgetting to await a coroutine (it never runs), blocking the "
            "event loop with synchronous I/O, and accidentally sharing mutable state between tasks."
        ),
        "examples": [
            {
                "title": "Concurrent HTTP requests with semaphore",
                "code": (
                    "import asyncio\n"
                    "import httpx\n\n"
                    "async def fetch(client, url, semaphore):\n"
                    "    async with semaphore:\n"
                    "        response = await client.get(url)\n"
                    "        return response.json()\n\n"
                    "async def fetch_all(urls, max_concurrent=10):\n"
                    "    semaphore = asyncio.Semaphore(max_concurrent)\n"
                    "    async with httpx.AsyncClient() as client:\n"
                    "        tasks = [fetch(client, url, semaphore) for url in urls]\n"
                    "        return await asyncio.gather(*tasks)\n\n"
                    "results = asyncio.run(fetch_all(urls))"
                ),
            },
            {
                "title": "TaskGroup for structured concurrency (Python 3.11+)",
                "code": (
                    "async def process_batch(items):\n"
                    "    results = []\n"
                    "    async with asyncio.TaskGroup() as tg:\n"
                    "        for item in items:\n"
                    "            task = tg.create_task(process_item(item))\n"
                    "            results.append(task)\n"
                    "    # All tasks completed; if any raised, ExceptionGroup is raised\n"
                    "    return [t.result() for t in results]"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Implement an async rate limiter that allows at most N requests per second using asyncio primitives.",
                "hint": "Use asyncio.Semaphore combined with a background task that releases permits every 1/N seconds, or use a token bucket pattern with asyncio.sleep.",
            },
            {
                "question": "Explain why asyncio.gather() can silently swallow exceptions by default and how to handle them properly.",
                "hint": "By default, if one task fails, gather cancels the rest and raises. With return_exceptions=True, exceptions are returned as values. Use TaskGroup for structured error handling.",
            },
        ],
        "tags": ["python", "asyncio", "async", "concurrency", "event-loop"],
    },

    # ========== DSA (3 lessons) ==========
    {
        "category": "dsa",
        "title": "Big-O Notation and Complexity Analysis",
        "slug": "big-o-notation-complexity-analysis",
        "difficulty": "beginner",
        "order_index": 1,
        "content": (
            "Big-O notation describes the upper bound of an algorithm's growth rate as the input size approaches "
            "infinity. It abstracts away constants and lower-order terms to focus on the dominant factor. When we "
            "say an algorithm is O(n log n), we mean its running time grows at most proportionally to n * log(n) "
            "for sufficiently large n. The formal definition: f(n) is O(g(n)) if there exist constants c > 0 and "
            "n0 such that f(n) <= c * g(n) for all n >= n0.\n\n"

            "The common complexity classes, from fastest to slowest: O(1) constant - hash table lookup, array "
            "access by index. O(log n) logarithmic - binary search, balanced BST operations. O(n) linear - "
            "scanning an array, linear search. O(n log n) linearithmic - merge sort, heap sort, most optimal "
            "comparison-based sorts. O(n^2) quadratic - nested loops, insertion sort, bubble sort. O(2^n) "
            "exponential - brute-force subset generation. O(n!) factorial - brute-force permutations.\n\n"

            "Space complexity measures the additional memory an algorithm requires beyond the input. In-place "
            "algorithms use O(1) extra space (like quicksort's partition). Merge sort uses O(n) extra space for "
            "the merge buffer. Recursive algorithms consume O(depth) stack space - a recursive DFS on a tree uses "
            "O(h) space where h is the tree height, which is O(log n) for balanced trees but O(n) for skewed ones. "
            "BFS uses O(w) space where w is the maximum width of the tree.\n\n"

            "Amortized analysis accounts for the average cost over a sequence of operations, even if individual "
            "operations are expensive. ArrayList's add() is O(1) amortized: most adds are O(1), but occasional "
            "resizing copies all elements at O(n). Since resizing doubles the capacity, the total cost of n "
            "insertions is O(n), giving O(1) amortized per insertion. Similarly, a splay tree has O(log n) amortized "
            "operations even though individual operations can be O(n).\n\n"

            "In interviews, always state both time and space complexity. For recursive solutions, express the "
            "recurrence relation: merge sort is T(n) = 2T(n/2) + O(n), which resolves to O(n log n) by the "
            "Master Theorem. Be prepared to analyze best case, worst case, and average case separately when they "
            "differ (e.g., quicksort: O(n log n) average, O(n^2) worst case with poor pivot selection)."
        ),
        "examples": [
            {
                "title": "Identifying nested loop complexity",
                "code": (
                    "// O(n^2) - each loop runs n times\n"
                    "for (int i = 0; i < n; i++)\n"
                    "    for (int j = 0; j < n; j++)\n"
                    "        process(i, j);\n\n"
                    "// O(n log n) - outer runs n, inner halves each time\n"
                    "for (int i = 0; i < n; i++)\n"
                    "    for (int j = 1; j < n; j *= 2)\n"
                    "        process(i, j);\n\n"
                    "// O(n) - inner loop total across all i is n\n"
                    "for (int i = 0; i < n; i++)\n"
                    "    for (int j = i; j < n; j += n)\n"
                    "        process(i, j);"
                ),
            },
            {
                "title": "Master Theorem application",
                "description": (
                    "T(n) = aT(n/b) + O(n^d). Compare log_b(a) with d:\n"
                    "- If log_b(a) < d: T(n) = O(n^d)\n"
                    "- If log_b(a) = d: T(n) = O(n^d * log n)\n"
                    "- If log_b(a) > d: T(n) = O(n^(log_b(a)))\n\n"
                    "Merge sort: a=2, b=2, d=1. log_2(2) = 1 = d, so O(n log n).\n"
                    "Binary search: a=1, b=2, d=0. log_2(1) = 0 = d, so O(log n)."
                ),
            },
        ],
        "exercises": [
            {
                "question": "What is the time complexity of building a heap from an array using the bottom-up (sift-down) approach? Explain why it is O(n) and not O(n log n).",
                "hint": "Most nodes are near the bottom. Leaves (n/2 nodes) do 0 work, the next level does 1 swap, etc. Sum the series: n/4 * 1 + n/8 * 2 + ... = O(n).",
            },
            {
                "question": "An algorithm processes all pairs (i, j) where i < j in an array of n elements. What is its time complexity?",
                "hint": "The number of pairs is n*(n-1)/2 = O(n^2). Each pair is processed once.",
            },
        ],
        "tags": ["dsa", "big-o", "complexity", "algorithms", "time-complexity"],
    },
    {
        "category": "dsa",
        "title": "Trees and Binary Search Trees",
        "slug": "trees-and-binary-search-trees",
        "difficulty": "intermediate",
        "order_index": 2,
        "content": (
            "Trees are hierarchical data structures fundamental to computer science. A binary tree has at most "
            "two children per node. Key tree types include: full binary trees (every node has 0 or 2 children), "
            "complete binary trees (all levels filled except possibly the last, filled left to right), and "
            "perfect binary trees (all internal nodes have two children and all leaves are at the same level). "
            "A complete binary tree with n nodes has height floor(log2(n)), and a perfect binary tree of height "
            "h has exactly 2^(h+1) - 1 nodes.\n\n"

            "Tree traversals come in four forms. In-order (left, root, right) produces sorted output for a BST. "
            "Pre-order (root, left, right) serializes the tree structure. Post-order (left, right, root) is "
            "used for deletion and expression evaluation. Level-order (BFS) processes nodes breadth-first using "
            "a queue. Each traversal has recursive and iterative implementations. The iterative in-order traversal "
            "uses a stack: push all left children, pop and process, then move to the right child. Morris traversal "
            "achieves O(1) space by temporarily threading the tree.\n\n"

            "A Binary Search Tree (BST) maintains the invariant: for every node, all keys in the left subtree "
            "are less, and all keys in the right subtree are greater. Search, insert, and delete are O(h) where "
            "h is the tree height. For a balanced BST, h = O(log n), but for a degenerate (skewed) BST, h = O(n). "
            "BST deletion has three cases: leaf node (just remove), one child (replace with child), and two "
            "children (replace with in-order successor or predecessor, then delete the successor).\n\n"

            "Self-balancing BSTs guarantee O(log n) height. AVL trees maintain the invariant that the height "
            "difference between left and right subtrees is at most 1, rebalancing via rotations (left, right, "
            "left-right, right-left). Red-black trees relax the balance constraint: the longest path is at most "
            "twice the shortest. Java's TreeMap and TreeSet use red-black trees. B-trees generalize BSTs to have "
            "multiple keys per node and are optimized for disk access in databases.\n\n"

            "Common interview patterns with trees include: finding the lowest common ancestor (LCA), checking "
            "if a tree is balanced, computing tree diameter, serialization/deserialization, converting a sorted "
            "array to a balanced BST, and validating BST properties. For the BST validation problem, the "
            "in-order traversal approach is clean: traverse in-order and verify the sequence is strictly increasing."
        ),
        "examples": [
            {
                "title": "Iterative in-order traversal with a stack",
                "code": (
                    "public List<Integer> inorderTraversal(TreeNode root) {\n"
                    "    List<Integer> result = new ArrayList<>();\n"
                    "    Deque<TreeNode> stack = new ArrayDeque<>();\n"
                    "    TreeNode curr = root;\n"
                    "    while (curr != null || !stack.isEmpty()) {\n"
                    "        while (curr != null) {\n"
                    "            stack.push(curr);\n"
                    "            curr = curr.left;\n"
                    "        }\n"
                    "        curr = stack.pop();\n"
                    "        result.add(curr.val);\n"
                    "        curr = curr.right;\n"
                    "    }\n"
                    "    return result;\n"
                    "}"
                ),
            },
            {
                "title": "BST validation using range checking",
                "code": (
                    "public boolean isValidBST(TreeNode node) {\n"
                    "    return validate(node, Long.MIN_VALUE, Long.MAX_VALUE);\n"
                    "}\n\n"
                    "private boolean validate(TreeNode node, long min, long max) {\n"
                    "    if (node == null) return true;\n"
                    "    if (node.val <= min || node.val >= max) return false;\n"
                    "    return validate(node.left, min, node.val)\n"
                    "        && validate(node.right, node.val, max);\n"
                    "}"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Given a BST, find the kth smallest element. What are the time and space complexities of your approach?",
                "hint": "Use in-order traversal (iterative with a stack). Stop after visiting k nodes. Time O(h + k), Space O(h).",
            },
            {
                "question": "How would you find the lowest common ancestor of two nodes in a BST versus a general binary tree?",
                "hint": "In a BST, use the values: if both are less, go left; if both are greater, go right; otherwise current node is the LCA. In a general tree, use recursive post-order.",
            },
        ],
        "tags": ["dsa", "trees", "bst", "binary-tree", "traversal"],
    },
    {
        "category": "dsa",
        "title": "Graph Algorithms - BFS, DFS, and Shortest Paths",
        "slug": "graph-algorithms-bfs-dfs-shortest-paths",
        "difficulty": "advanced",
        "order_index": 3,
        "content": (
            "Graphs are one of the most versatile data structures, modeling networks, relationships, and "
            "dependencies. A graph G = (V, E) consists of vertices V and edges E. Graphs can be directed or "
            "undirected, weighted or unweighted, and cyclic or acyclic. Representation choices matter: an "
            "adjacency list uses O(V + E) space and is efficient for sparse graphs, while an adjacency matrix "
            "uses O(V^2) space but provides O(1) edge lookup. For most interview and production scenarios, "
            "adjacency lists (Map<Node, List<Node>>) are preferred.\n\n"

            "Breadth-First Search (BFS) explores the graph level by level using a queue. Starting from a source "
            "vertex, BFS visits all neighbors before moving to their neighbors. This guarantees finding the "
            "shortest path in unweighted graphs (shortest by number of edges). BFS runs in O(V + E) time. "
            "Common applications include: shortest path in unweighted graphs, finding connected components, "
            "detecting cycles in undirected graphs (via parent tracking), and multi-source BFS (add all sources "
            "to the initial queue) for problems like 'rotting oranges'.\n\n"

            "Depth-First Search (DFS) explores as deep as possible before backtracking, using a stack (explicit "
            "or the call stack). DFS also runs in O(V + E). It is used for topological sorting (process a node "
            "only after all its dependencies), detecting cycles in directed graphs (back edges in the DFS tree), "
            "finding strongly connected components (Tarjan's or Kosaraju's algorithm), and solving problems "
            "that require exploring all paths (backtracking). The three edge types in a DFS tree - tree edges, "
            "back edges, and cross/forward edges - provide structural information about the graph.\n\n"

            "Dijkstra's algorithm finds the shortest path from a source to all other vertices in a weighted "
            "graph with non-negative edges. It uses a priority queue (min-heap) to always process the vertex "
            "with the smallest known distance. Time complexity is O((V + E) log V) with a binary heap. Dijkstra "
            "fails with negative edges because it assumes a processed vertex's distance is final. For negative "
            "edges (but no negative cycles), use Bellman-Ford at O(VE). For all-pairs shortest paths, use Floyd-"
            "Warshall at O(V^3).\n\n"

            "Topological sort orders vertices in a directed acyclic graph (DAG) such that for every edge u -> v, "
            "u appears before v. Two approaches: Kahn's algorithm (BFS with in-degree tracking) and DFS-based "
            "(post-order reversal). Kahn's algorithm also detects cycles: if the sorted output has fewer than V "
            "vertices, a cycle exists. Applications include build systems, task scheduling, course prerequisites, "
            "and dependency resolution."
        ),
        "examples": [
            {
                "title": "BFS shortest path in unweighted graph",
                "code": (
                    "public int shortestPath(Map<Integer, List<Integer>> graph,\n"
                    "                        int source, int target) {\n"
                    "    Queue<Integer> queue = new LinkedList<>();\n"
                    "    Set<Integer> visited = new HashSet<>();\n"
                    "    queue.offer(source);\n"
                    "    visited.add(source);\n"
                    "    int distance = 0;\n"
                    "    while (!queue.isEmpty()) {\n"
                    "        int size = queue.size();\n"
                    "        for (int i = 0; i < size; i++) {\n"
                    "            int node = queue.poll();\n"
                    "            if (node == target) return distance;\n"
                    "            for (int neighbor : graph.getOrDefault(node, List.of())) {\n"
                    "                if (visited.add(neighbor)) {\n"
                    "                    queue.offer(neighbor);\n"
                    "                }\n"
                    "            }\n"
                    "        }\n"
                    "        distance++;\n"
                    "    }\n"
                    "    return -1;\n"
                    "}"
                ),
            },
            {
                "title": "Topological sort with Kahn's algorithm",
                "code": (
                    "public List<Integer> topologicalSort(int n, int[][] edges) {\n"
                    "    int[] inDegree = new int[n];\n"
                    "    Map<Integer, List<Integer>> graph = new HashMap<>();\n"
                    "    for (int[] e : edges) {\n"
                    "        graph.computeIfAbsent(e[0], k -> new ArrayList<>()).add(e[1]);\n"
                    "        inDegree[e[1]]++;\n"
                    "    }\n"
                    "    Queue<Integer> queue = new LinkedList<>();\n"
                    "    for (int i = 0; i < n; i++)\n"
                    "        if (inDegree[i] == 0) queue.offer(i);\n"
                    "    List<Integer> result = new ArrayList<>();\n"
                    "    while (!queue.isEmpty()) {\n"
                    "        int node = queue.poll();\n"
                    "        result.add(node);\n"
                    "        for (int neighbor : graph.getOrDefault(node, List.of())) {\n"
                    "            if (--inDegree[neighbor] == 0) queue.offer(neighbor);\n"
                    "        }\n"
                    "    }\n"
                    "    return result.size() == n ? result : List.of(); // empty = cycle\n"
                    "}"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Given a list of courses and prerequisites, determine if it is possible to finish all courses. What is the algorithm?",
                "hint": "Model as a directed graph. If a topological sort includes all courses, there is no cycle and all courses can be completed.",
            },
            {
                "question": "Modify Dijkstra's algorithm to also track the actual shortest path (not just the distance). What data structure do you add?",
                "hint": "Maintain a predecessor map: when you relax an edge (u, v), record prev[v] = u. Reconstruct the path by following predecessors from target to source.",
            },
        ],
        "tags": ["dsa", "graphs", "bfs", "dfs", "dijkstra", "topological-sort"],
    },

    # ========== SYSTEM DESIGN (2 lessons) ==========
    {
        "category": "system_design",
        "title": "CAP Theorem and Consistency Models",
        "slug": "cap-theorem-consistency-models",
        "difficulty": "advanced",
        "order_index": 1,
        "content": (
            "The CAP theorem, proven by Eric Brewer, states that a distributed data store can provide at most two "
            "of three guarantees simultaneously: Consistency (every read returns the most recent write), "
            "Availability (every request receives a non-error response), and Partition tolerance (the system "
            "continues to operate despite network partitions between nodes). Since network partitions are "
            "unavoidable in any distributed system, the real choice is between consistency and availability "
            "during a partition: CP systems (like HBase, MongoDB with majority read concern) reject requests that "
            "cannot be confirmed consistent, while AP systems (like Cassandra, DynamoDB) serve potentially stale "
            "data to remain available.\n\n"

            "The CAP theorem is often oversimplified. In practice, you choose on a per-operation basis, not "
            "per-system. Cassandra, classified as AP, supports tunable consistency: a read with quorum consistency "
            "(R + W > N) provides strong consistency for that specific read. DynamoDB offers both eventually "
            "consistent reads and strongly consistent reads at different latency/cost profiles. The PACELC "
            "theorem extends CAP: when there is no Partition, you trade between Latency and Consistency. This "
            "explains why systems like Cassandra choose lower latency (eventual consistency) even when the network "
            "is healthy.\n\n"

            "Consistency models define the contract between a distributed system and its clients. Strong "
            "consistency (linearizability) means operations appear to happen atomically at a single point in time: "
            "once a write completes, all subsequent reads see it. Sequential consistency is weaker: operations "
            "from each client appear in order, but there is no global time ordering. Causal consistency ensures "
            "that causally related operations are seen in order, while concurrent operations may be seen in any "
            "order. Eventual consistency is the weakest useful model: given no new writes, all replicas will "
            "eventually converge to the same value.\n\n"

            "In practice, most production systems use eventual consistency with conflict resolution strategies. "
            "Last-Writer-Wins (LWW) uses timestamps to resolve conflicts but can lose updates (clock skew). "
            "Vector clocks detect concurrent writes but are complex to manage. CRDTs (Conflict-free Replicated "
            "Data Types) are data structures that can be merged automatically without coordination - counters, "
            "sets, and registers that converge by mathematical guarantee. Riak and Redis Enterprise use CRDTs "
            "for multi-datacenter replication.\n\n"

            "When designing systems in interviews, always clarify the consistency requirement. A banking system "
            "needs strong consistency for account balances. A social media feed can tolerate eventual consistency. "
            "A shopping cart might use session consistency (read your own writes). Articulate the trade-off: "
            "stronger consistency increases latency and reduces availability during partitions."
        ),
        "examples": [
            {
                "title": "Tunable consistency in Cassandra",
                "description": (
                    "Cassandra uses replication factor (N), write consistency (W), and read consistency (R):\n"
                    "- ONE: fastest, least consistent - write to any single replica\n"
                    "- QUORUM: majority of replicas must acknowledge (N/2 + 1)\n"
                    "- ALL: all replicas must acknowledge - slowest, most consistent\n\n"
                    "Strong consistency: R + W > N. Example: N=3, R=QUORUM(2), W=QUORUM(2).\n"
                    "Read-heavy optimization: N=3, W=ALL(3), R=ONE(1) - also consistent.\n"
                    "Write-heavy: N=3, W=ONE(1), R=ALL(3) - also consistent."
                ),
            },
            {
                "title": "Read-your-writes consistency pattern",
                "code": (
                    "// After a write, ensure the same user reads from\n"
                    "// the leader (not a stale replica) for a window\n"
                    "class ReadYourWritesProxy {\n"
                    "    private final Map<String, Instant> lastWriteTime;\n"
                    "    private final Duration staleness = Duration.ofSeconds(5);\n\n"
                    "    public Data read(String userId, String key) {\n"
                    "        Instant lastWrite = lastWriteTime.get(userId);\n"
                    "        if (lastWrite != null && lastWrite.isAfter(\n"
                    "                Instant.now().minus(staleness))) {\n"
                    "            return readFromLeader(key);\n"
                    "        }\n"
                    "        return readFromReplica(key);\n"
                    "    }\n"
                    "}"
                ),
            },
        ],
        "exercises": [
            {
                "question": "You are designing a distributed counter (e.g., page view count) that must be accurate within 1% and handle 100K increments per second. Which consistency model do you use and why?",
                "hint": "Eventual consistency with a G-Counter CRDT or sharded counters that periodically merge. Strong consistency would be too slow at that throughput.",
            },
            {
                "question": "Explain why a distributed lock service like ZooKeeper chooses CP over AP. What happens during a network partition?",
                "hint": "A lock must be exclusive. If two nodes both believe they hold the lock (AP behavior), the mutual exclusion guarantee is broken. During a partition, the minority partition becomes unavailable.",
            },
        ],
        "tags": ["system-design", "cap-theorem", "consistency", "distributed-systems", "trade-offs"],
    },
    {
        "category": "system_design",
        "title": "Caching Strategies and Patterns",
        "slug": "caching-strategies-patterns",
        "difficulty": "intermediate",
        "order_index": 2,
        "content": (
            "Caching is one of the most impactful performance optimizations in system design. A cache stores "
            "frequently accessed data in a faster storage tier (memory vs. disk, local vs. remote) to reduce "
            "latency, decrease database load, and improve throughput. The fundamental trade-off is between "
            "freshness and speed: cached data may be stale. Choosing the right caching strategy determines "
            "how stale data can get and how writes are handled.\n\n"

            "Cache-Aside (Lazy Loading) is the most common pattern. The application checks the cache first; on "
            "a miss, it reads from the database, populates the cache, and returns the data. Writes go directly "
            "to the database, and the cache entry is either invalidated or updated. Advantages: only requested "
            "data is cached, cache failures are non-fatal (fall back to DB). Disadvantages: initial requests are "
            "always slow (cold cache), and there is a window of inconsistency between cache and DB.\n\n"

            "Write-Through writes to the cache and the database synchronously in the same operation. The cache "
            "is always consistent with the database. Combined with read-through (the cache itself handles misses "
            "by loading from DB), this provides a simple programming model. The downside is higher write latency "
            "since every write hits both stores. Write-Behind (Write-Back) defers the database write: data is "
            "written to the cache immediately and asynchronously flushed to the database. This reduces write "
            "latency and batches writes, but risks data loss if the cache crashes before flushing.\n\n"

            "Cache eviction policies determine which entries to remove when the cache is full. LRU (Least "
            "Recently Used) evicts the entry that has not been accessed for the longest time. LFU (Least "
            "Frequently Used) evicts the entry with the fewest accesses. TTL (Time To Live) removes entries "
            "after a fixed duration regardless of access patterns. In practice, LRU with TTL is the most common "
            "combination. Redis supports volatile-lru (evict keys with TTL set), allkeys-lru, volatile-ttl, and "
            "noeviction policies.\n\n"

            "Cache invalidation is famously hard. The two main approaches are: event-driven invalidation (publish "
            "a cache-invalidation event when data changes) and TTL-based expiration (accept bounded staleness). "
            "Stampede protection prevents multiple concurrent cache misses for the same key from overloading the "
            "database: use a distributed lock so only one request populates the cache, or implement request "
            "coalescing. Cache warming pre-populates the cache with expected hot data before deploying a new "
            "cache instance to avoid cold-start latency spikes."
        ),
        "examples": [
            {
                "title": "Cache-Aside pattern with Redis in Spring Boot",
                "code": (
                    "@Service\n"
                    "public class ProductService {\n"
                    "    @Cacheable(value = \"products\", key = \"#id\",\n"
                    "              unless = \"#result == null\")\n"
                    "    public Product getProduct(Long id) {\n"
                    "        return productRepository.findById(id).orElse(null);\n"
                    "    }\n\n"
                    "    @CacheEvict(value = \"products\", key = \"#product.id\")\n"
                    "    public Product updateProduct(Product product) {\n"
                    "        return productRepository.save(product);\n"
                    "    }\n\n"
                    "    @CacheEvict(value = \"products\", allEntries = true)\n"
                    "    @Scheduled(fixedRate = 3600000) // hourly\n"
                    "    public void evictAllProducts() {\n"
                    "        LOG.info(\"Evicting all product cache entries\");\n"
                    "    }\n"
                    "}"
                ),
            },
            {
                "title": "Stampede protection with distributed lock",
                "code": (
                    "public Product getProductWithStampedeProtection(Long id) {\n"
                    "    Product cached = cache.get(\"product:\" + id);\n"
                    "    if (cached != null) return cached;\n\n"
                    "    String lockKey = \"lock:product:\" + id;\n"
                    "    boolean acquired = redis.setNx(lockKey, \"1\",\n"
                    "        Duration.ofSeconds(5));\n"
                    "    if (acquired) {\n"
                    "        try {\n"
                    "            Product product = productRepository.findById(id)\n"
                    "                .orElse(null);\n"
                    "            cache.put(\"product:\" + id, product,\n"
                    "                Duration.ofMinutes(10));\n"
                    "            return product;\n"
                    "        } finally {\n"
                    "            redis.delete(lockKey);\n"
                    "        }\n"
                    "    }\n"
                    "    // Another thread is loading; wait and retry\n"
                    "    Thread.sleep(50);\n"
                    "    return getProductWithStampedeProtection(id);\n"
                    "}"
                ),
            },
        ],
        "exercises": [
            {
                "question": "You have a product catalog with 1M items. 1% of items get 90% of traffic. Design a multi-level caching strategy with local (in-process) and distributed (Redis) caches.",
                "hint": "Use a small local Caffeine cache (10K items, TTL 30s) as L1 and Redis as L2. Local cache reduces network hops for the hottest items. Use pub/sub to invalidate L1 entries across instances.",
            },
            {
                "question": "Explain the differences between cache invalidation and cache expiration. When would you prefer one over the other?",
                "hint": "Invalidation actively removes entries on data change (strong consistency). Expiration uses TTL and accepts bounded staleness. Use invalidation for transactional data, expiration for data where slight staleness is acceptable.",
            },
        ],
        "tags": ["system-design", "caching", "redis", "performance", "write-through", "cache-aside"],
    },

    # ========== DISTRIBUTED SYSTEMS (2 lessons) ==========
    {
        "category": "distributed",
        "title": "Consensus Algorithms - Paxos and Raft",
        "slug": "consensus-algorithms-paxos-raft",
        "difficulty": "advanced",
        "order_index": 1,
        "content": (
            "Consensus is the fundamental problem in distributed computing: getting multiple nodes to agree on "
            "a single value despite failures. This is essential for leader election, distributed locks, "
            "configuration management, and replicated state machines. The FLP impossibility result proves that "
            "no deterministic consensus algorithm can guarantee termination in an asynchronous system with even "
            "one crash failure, but practical algorithms work around this by using timeouts to detect failures "
            "(partial synchrony assumption).\n\n"

            "Paxos, developed by Leslie Lamport, is the foundational consensus algorithm. It operates in two "
            "phases. In Phase 1 (Prepare), a proposer sends a prepare request with a unique proposal number n "
            "to a majority of acceptors. Each acceptor promises not to accept any proposal with a number less "
            "than n and returns the highest-numbered proposal it has already accepted. In Phase 2 (Accept), the "
            "proposer picks the value from the highest-numbered accepted proposal (or its own value if none) "
            "and sends an accept request. If a majority of acceptors accept, consensus is reached. Multi-Paxos "
            "optimizes for a sequence of decisions by electing a stable leader that skips Phase 1.\n\n"

            "Raft, designed by Diego Ongaro, achieves the same safety guarantees as Paxos but with a more "
            "understandable decomposition. Raft breaks consensus into three sub-problems: leader election, log "
            "replication, and safety. The cluster elects a single leader via randomized election timeouts. The "
            "leader receives client requests, appends them to its log, replicates entries to followers, and "
            "commits when a majority have acknowledged. If the leader fails, followers that time out without a "
            "heartbeat start a new election term.\n\n"

            "Raft's log matching property ensures that if two logs contain an entry with the same index and "
            "term, all preceding entries are identical. The leader forces followers to match its log, overwriting "
            "any divergent entries. A new leader is guaranteed to have all committed entries because a candidate "
            "must receive votes from a majority, and any majority overlaps with the set of nodes that acknowledged "
            "a committed entry. This property is the core safety guarantee.\n\n"

            "In production, etcd (Kubernetes' backing store) uses Raft, as does CockroachDB and TiKV. ZooKeeper "
            "uses ZAB (a Paxos variant). When designing systems that need consensus, prefer using an existing "
            "implementation (etcd, ZooKeeper, Consul) rather than building your own. In interviews, focus on: "
            "why consensus needs a majority (to ensure overlap), how leader election works, what happens during "
            "a network partition (the majority partition elects a new leader; the minority cannot make progress), "
            "and the performance implications (writes require a majority round-trip)."
        ),
        "examples": [
            {
                "title": "Raft leader election flow",
                "description": (
                    "1. All nodes start as followers with a randomized election timeout (150-300ms)\n"
                    "2. If a follower receives no heartbeat before timeout, it becomes a candidate\n"
                    "3. Candidate increments its term, votes for itself, sends RequestVote RPCs\n"
                    "4. Other nodes vote yes if: candidate's term >= their term, AND candidate's "
                    "log is at least as up-to-date (last entry's term and index)\n"
                    "5. Candidate receiving majority votes becomes leader\n"
                    "6. Leader sends periodic heartbeats (AppendEntries with no entries) to prevent "
                    "new elections\n"
                    "7. If two candidates split the vote, both time out and retry with new terms"
                ),
            },
            {
                "title": "Raft log replication",
                "description": (
                    "1. Client sends a write request to the leader\n"
                    "2. Leader appends the entry to its log with the current term number\n"
                    "3. Leader sends AppendEntries RPCs to all followers in parallel\n"
                    "4. Each follower checks: does it have the entry at prevLogIndex with "
                    "prevLogTerm? If yes, append and ack. If no, reject (leader will decrement "
                    "nextIndex and retry)\n"
                    "5. Once a majority of followers ack, the leader commits the entry\n"
                    "6. Leader applies the committed entry to its state machine and responds to client\n"
                    "7. Followers learn of the commit via the next AppendEntries and apply it"
                ),
            },
        ],
        "exercises": [
            {
                "question": "In a 5-node Raft cluster, what is the maximum number of node failures the system can tolerate while still making progress?",
                "hint": "A majority is 3. The system can tolerate 2 failures and still have a quorum of 3 to elect a leader and commit entries.",
            },
            {
                "question": "Explain a split-brain scenario and how Raft prevents it.",
                "hint": "If the network partitions into two groups, at most one group has a majority and can elect a leader. The minority group's old leader will step down when it receives messages with a higher term.",
            },
        ],
        "tags": ["distributed-systems", "consensus", "raft", "paxos", "leader-election"],
    },
    {
        "category": "distributed",
        "title": "Event Sourcing and CQRS",
        "slug": "event-sourcing-and-cqrs",
        "difficulty": "advanced",
        "order_index": 2,
        "content": (
            "Event Sourcing is an architectural pattern where the state of an application is determined by a "
            "sequence of events rather than by the current state alone. Instead of storing the latest state in a "
            "database row and overwriting it on each update, every state change is captured as an immutable event "
            "appended to an event store. To reconstruct the current state, you replay all events from the "
            "beginning (or from a snapshot). This provides a complete audit trail, enables temporal queries "
            "(what was the state at time T?), and supports undo operations naturally.\n\n"

            "Events are facts about what happened: OrderPlaced, PaymentReceived, ItemShipped. They are named in "
            "the past tense and are immutable - you never update or delete an event. Each event carries the data "
            "necessary to understand the change: OrderPlaced includes the order ID, customer ID, items, and "
            "prices. The aggregate is the consistency boundary: an event stream belongs to a single aggregate, "
            "and commands are validated against the aggregate's current state before events are emitted. "
            "Concurrency control uses optimistic locking on the aggregate's version number.\n\n"

            "CQRS (Command Query Responsibility Segregation) separates the write model (commands that produce "
            "events) from the read model (projections optimized for queries). The write side validates commands "
            "and appends events. The read side subscribes to events and builds denormalized views tailored to "
            "specific query patterns - a flat table for listing, a search index for full-text search, a "
            "materialized view for dashboards. This separation allows each side to scale independently and use "
            "the most appropriate storage technology.\n\n"

            "Event Sourcing with CQRS introduces eventual consistency between the write and read sides. After "
            "an event is stored, projections are updated asynchronously. This means a read immediately after a "
            "write may return stale data. Techniques to mitigate this include: read-after-write consistency "
            "(return the command result directly), polling (client polls until the projection catches up), and "
            "versioning (include the event sequence number and let the client wait).\n\n"

            "Challenges include: event schema evolution (how do you handle events when the schema changes? Use "
            "upcasters to transform old events to the new schema), performance of replaying long event streams "
            "(solved by snapshotting - periodically save the aggregate state and replay only from the latest "
            "snapshot), and the complexity of managing multiple projections. Despite these challenges, event "
            "sourcing excels in domains where auditability, temporal queries, and complex event processing are "
            "required - financial systems, compliance, and collaborative editing."
        ),
        "examples": [
            {
                "title": "Event sourcing aggregate in Java",
                "code": (
                    "public class OrderAggregate {\n"
                    "    private UUID orderId;\n"
                    "    private OrderStatus status;\n"
                    "    private List<OrderItem> items;\n"
                    "    private int version;\n\n"
                    "    // Reconstruct from events\n"
                    "    public static OrderAggregate fromEvents(List<Event> events) {\n"
                    "        OrderAggregate order = new OrderAggregate();\n"
                    "        events.forEach(order::apply);\n"
                    "        return order;\n"
                    "    }\n\n"
                    "    // Command handler\n"
                    "    public List<Event> handle(CancelOrderCommand cmd) {\n"
                    "        if (status == OrderStatus.SHIPPED)\n"
                    "            throw new IllegalStateException(\"Cannot cancel shipped\");\n"
                    "        return List.of(new OrderCancelled(orderId, cmd.reason()));\n"
                    "    }\n\n"
                    "    // Event applicator\n"
                    "    private void apply(Event event) {\n"
                    "        if (event instanceof OrderPlaced e) {\n"
                    "            this.orderId = e.orderId();\n"
                    "            this.status = OrderStatus.PLACED;\n"
                    "            this.items = e.items();\n"
                    "        } else if (event instanceof OrderCancelled e) {\n"
                    "            this.status = OrderStatus.CANCELLED;\n"
                    "        }\n"
                    "        this.version++;\n"
                    "    }\n"
                    "}"
                ),
            },
            {
                "title": "CQRS read-side projection",
                "code": (
                    "@Component\n"
                    "public class OrderSummaryProjection {\n"
                    "    private final OrderSummaryRepository repo;\n\n"
                    "    @EventHandler\n"
                    "    public void on(OrderPlaced event) {\n"
                    "        repo.save(new OrderSummary(\n"
                    "            event.orderId(), event.customerId(),\n"
                    "            event.totalAmount(), \"PLACED\",\n"
                    "            event.timestamp()));\n"
                    "    }\n\n"
                    "    @EventHandler\n"
                    "    public void on(OrderShipped event) {\n"
                    "        repo.updateStatus(event.orderId(), \"SHIPPED\");\n"
                    "    }\n"
                    "}"
                ),
            },
        ],
        "exercises": [
            {
                "question": "How would you handle event schema evolution when an OrderPlaced event needs a new required field (shippingAddress) that old events do not have?",
                "hint": "Write an upcaster that transforms V1 events to V2, supplying a default shippingAddress. Never modify stored events. Alternatively, use a new event name (OrderPlacedV2).",
            },
            {
                "question": "Your event stream for a single aggregate has grown to 10,000 events. Replaying takes 2 seconds. How do you improve this?",
                "hint": "Implement snapshotting: periodically serialize the aggregate state and store it alongside the event. To reconstruct, load the latest snapshot and replay only events after it.",
            },
        ],
        "tags": ["distributed-systems", "event-sourcing", "cqrs", "architecture", "patterns"],
    },

    # ========== AWS (2 lessons) ==========
    {
        "category": "aws",
        "title": "AWS Lambda and Serverless Architecture",
        "slug": "aws-lambda-serverless-architecture",
        "difficulty": "intermediate",
        "order_index": 1,
        "content": (
            "AWS Lambda is a serverless compute service that runs your code in response to events without "
            "provisioning or managing servers. You upload a function (a deployment package up to 50MB compressed "
            "or 250MB uncompressed), configure a trigger (API Gateway, S3 event, SQS message, CloudWatch "
            "schedule, DynamoDB stream), and Lambda handles scaling, patching, and availability. You pay only "
            "for the compute time consumed, billed in 1ms increments, making it cost-effective for sporadic "
            "or bursty workloads.\n\n"

            "Lambda execution model: when an event arrives, Lambda provisions an execution environment (a "
            "lightweight microVM via Firecracker), initializes the runtime, and invokes your handler function. "
            "The environment may be reused for subsequent invocations (warm start) or destroyed and recreated "
            "(cold start). Cold starts add latency - typically 100ms-2s for JVM-based runtimes and 50-200ms "
            "for Python/Node. Strategies to minimize cold starts include: using provisioned concurrency (pre-"
            "warms N instances), choosing lightweight runtimes (Python, Node over Java), reducing deployment "
            "package size, and using Lambda SnapStart (Java) which snapshots the initialized VM.\n\n"

            "Lambda limits are important to know: 15-minute maximum execution time, 10GB memory (CPU scales "
            "proportionally), 1000 concurrent executions per region (soft limit, can be raised), 6MB synchronous "
            "payload, 256KB asynchronous payload, and /tmp provides 512MB-10GB of ephemeral storage. For "
            "workloads exceeding these limits, consider ECS Fargate or Step Functions for orchestration.\n\n"

            "Common serverless patterns include: API Gateway + Lambda for REST APIs, S3 events + Lambda for "
            "file processing, SQS + Lambda for async task processing, DynamoDB Streams + Lambda for change data "
            "capture, and EventBridge + Lambda for event-driven architectures. Step Functions orchestrate complex "
            "workflows by chaining Lambda functions with retry, parallel execution, and error handling.\n\n"

            "Serverless trade-offs: advantages include zero server management, automatic scaling to zero, pay-"
            "per-use pricing, and rapid deployment. Disadvantages include cold start latency, vendor lock-in, "
            "limited execution duration, debugging complexity (distributed tracing with X-Ray is essential), "
            "and the challenge of local development (SAM CLI and LocalStack help). Serverless is ideal for "
            "event-driven workloads, APIs with variable traffic, and data processing pipelines. It is less "
            "suited for long-running computations, WebSocket servers, or latency-sensitive applications."
        ),
        "examples": [
            {
                "title": "Lambda handler with SQS trigger (Python)",
                "code": (
                    "import json\n"
                    "import boto3\n\n"
                    "dynamodb = boto3.resource('dynamodb')\n"
                    "table = dynamodb.Table('orders')\n\n"
                    "def handler(event, context):\n"
                    "    for record in event['Records']:\n"
                    "        body = json.loads(record['body'])\n"
                    "        order_id = body['orderId']\n"
                    "        try:\n"
                    "            table.put_item(Item={\n"
                    "                'orderId': order_id,\n"
                    "                'status': 'PROCESSING',\n"
                    "                'items': body['items'],\n"
                    "            })\n"
                    "        except Exception as e:\n"
                    "            print(f'Failed to process {order_id}: {e}')\n"
                    "            raise  # SQS will retry\n"
                    "    return {'statusCode': 200}"
                ),
            },
            {
                "title": "SAM template for API Gateway + Lambda",
                "code": (
                    "AWSTemplateFormatVersion: '2010-09-09'\n"
                    "Transform: AWS::Serverless-2016-10-31\n\n"
                    "Resources:\n"
                    "  ApiFunction:\n"
                    "    Type: AWS::Serverless::Function\n"
                    "    Properties:\n"
                    "      Runtime: python3.12\n"
                    "      Handler: app.handler\n"
                    "      MemorySize: 256\n"
                    "      Timeout: 30\n"
                    "      Events:\n"
                    "        GetOrder:\n"
                    "          Type: Api\n"
                    "          Properties:\n"
                    "            Path: /orders/{id}\n"
                    "            Method: GET"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Design an image processing pipeline: users upload images to S3, and you need to generate thumbnails in three sizes. How would you architect this with Lambda?",
                "hint": "S3 PUT event triggers Lambda. Lambda reads the original image, generates three thumbnails, and writes them to an output bucket. Use /tmp for scratch space. For images > 512MB, consider Step Functions with Fargate.",
            },
            {
                "question": "Your Lambda function processes SQS messages but occasionally fails. How do you handle retries and dead-letter queues?",
                "hint": "SQS automatically retries failed messages (visibility timeout). Configure a DLQ (dead-letter queue) with maxReceiveCount=3 so messages that fail 3 times are moved to the DLQ for investigation.",
            },
        ],
        "tags": ["aws", "lambda", "serverless", "api-gateway", "cloud"],
    },
    {
        "category": "aws",
        "title": "SQS and Event-Driven Architecture",
        "slug": "sqs-event-driven-architecture",
        "difficulty": "intermediate",
        "order_index": 2,
        "content": (
            "Amazon SQS (Simple Queue Service) is a fully managed message queue that decouples producers from "
            "consumers. It provides two queue types: Standard queues offer best-effort ordering and at-least-once "
            "delivery with nearly unlimited throughput. FIFO queues guarantee exactly-once processing and strict "
            "ordering within message groups, at up to 3,000 messages per second (with batching). Choosing between "
            "them depends on your requirements: use Standard for high-throughput workloads that can handle "
            "duplicates, FIFO for order-sensitive workflows like financial transactions.\n\n"

            "SQS message lifecycle: a producer sends a message, which becomes available after an optional delay "
            "(up to 15 minutes). A consumer receives the message, which becomes invisible for the visibility "
            "timeout period (default 30 seconds, configurable up to 12 hours). The consumer processes the "
            "message and deletes it. If the consumer crashes before deleting, the message becomes visible again "
            "after the timeout expires and another consumer picks it up. This at-least-once delivery model means "
            "consumers must be idempotent.\n\n"

            "Dead-letter queues (DLQs) capture messages that fail processing after a configured number of "
            "receive attempts (maxReceiveCount). This prevents poison messages from blocking the queue "
            "indefinitely. You should set up CloudWatch alarms on the DLQ's ApproximateNumberOfMessagesVisible "
            "metric to alert when messages land there. SQS also supports message attributes (metadata), message "
            "timers (per-message delay), long polling (reduces empty responses and costs), and server-side "
            "encryption with KMS.\n\n"

            "Event-driven architecture (EDA) uses events as the primary communication mechanism between services. "
            "Services publish events to a message broker (SNS, EventBridge, Kafka) and other services subscribe. "
            "This decouples services temporally (producer does not wait for consumer) and spatially (producer does "
            "not know about consumers). SNS + SQS (fan-out) is a powerful pattern: an SNS topic publishes to "
            "multiple SQS queues, each serving a different consumer. This allows adding new consumers without "
            "modifying the producer.\n\n"

            "EventBridge is AWS's serverless event bus that supports content-based filtering (rules that match "
            "event patterns), schema discovery, and cross-account/cross-region event routing. It is the preferred "
            "choice for complex event routing over SNS when you need fine-grained filtering or event "
            "transformation. For high-throughput event streaming with replay capability, Amazon Kinesis Data "
            "Streams or MSK (Managed Kafka) are better choices, as SQS does not support event replay once a "
            "message is deleted."
        ),
        "examples": [
            {
                "title": "SNS + SQS fan-out pattern",
                "description": (
                    "Architecture:\n"
                    "- OrderService publishes 'OrderPlaced' to SNS topic\n"
                    "- SQS Queue 1 (InventoryService) subscribes to process stock updates\n"
                    "- SQS Queue 2 (NotificationService) subscribes to send email\n"
                    "- SQS Queue 3 (AnalyticsService) subscribes to update dashboards\n\n"
                    "Benefits:\n"
                    "- OrderService does not know about downstream consumers\n"
                    "- Adding a new consumer = create queue + subscribe to topic\n"
                    "- Each consumer processes at its own pace\n"
                    "- Consumer failure does not affect other consumers"
                ),
            },
            {
                "title": "Idempotent SQS consumer with DynamoDB",
                "code": (
                    "def process_message(message):\n"
                    "    message_id = message['MessageId']\n"
                    "    try:\n"
                    "        # Conditional put fails if message_id already processed\n"
                    "        table.put_item(\n"
                    "            Item={'messageId': message_id, 'processedAt': now()},\n"
                    "            ConditionExpression='attribute_not_exists(messageId)'\n"
                    "        )\n"
                    "    except ClientError as e:\n"
                    "        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':\n"
                    "            return  # Already processed, skip\n"
                    "        raise\n"
                    "    # Process the actual business logic\n"
                    "    handle_order(json.loads(message['Body']))"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Design a system where 10 microservices need to react to user registration events. Some need guaranteed delivery, others are best-effort. How do you architect the messaging?",
                "hint": "SNS topic for fan-out. Critical services subscribe via SQS with DLQs. Best-effort services subscribe directly to SNS (HTTP endpoint) or use EventBridge with retry policies.",
            },
            {
                "question": "Your SQS consumer processes messages but occasionally takes longer than the visibility timeout, causing duplicate processing. How do you fix this?",
                "hint": "Increase the visibility timeout. Use ChangeMessageVisibility to extend it during processing. Implement idempotency so duplicates are harmless.",
            },
        ],
        "tags": ["aws", "sqs", "sns", "event-driven", "messaging", "decoupling"],
    },

    # ========== AZURE (1 lesson) ==========
    {
        "category": "azure",
        "title": "Azure Kubernetes Service (AKS) Deep Dive",
        "slug": "azure-kubernetes-service-aks",
        "difficulty": "advanced",
        "order_index": 1,
        "content": (
            "Azure Kubernetes Service (AKS) is a managed Kubernetes offering where Azure handles the control "
            "plane (API server, etcd, scheduler, controller manager) at no charge - you pay only for the worker "
            "nodes. AKS integrates deeply with Azure services: Azure Active Directory for RBAC, Azure Monitor "
            "and Log Analytics for observability, Azure Container Registry (ACR) for image storage, Azure Key "
            "Vault for secrets management, and Azure Disk/Files for persistent storage.\n\n"

            "Node pools are groups of VMs that run your pods. AKS supports system node pools (for Kubernetes "
            "system pods like CoreDNS and kube-proxy) and user node pools (for application workloads). You can "
            "have multiple node pools with different VM sizes to match workload requirements: CPU-optimized for "
            "compute-heavy services, memory-optimized for caching layers, and GPU-enabled for ML workloads. "
            "The cluster autoscaler automatically adjusts node pool size based on pending pods, while the "
            "Horizontal Pod Autoscaler (HPA) scales pod replicas based on CPU, memory, or custom metrics.\n\n"

            "Networking in AKS offers two models: kubenet (basic) assigns pod IPs from a separate address space "
            "with NAT for external communication, while Azure CNI (advanced) assigns pod IPs directly from the "
            "Azure VNet subnet, enabling direct communication with other Azure resources without NAT. Azure CNI "
            "is recommended for production because it supports Network Policies (Calico or Azure Network Policy), "
            "direct VNet integration, and Azure Private Link. Ingress can be handled by NGINX Ingress Controller, "
            "Application Gateway Ingress Controller (AGIC), or the newer Istio-based service mesh add-on.\n\n"

            "Security best practices for AKS: enable Azure AD integration for kubectl authentication, use "
            "Kubernetes RBAC with Azure AD groups, store secrets in Azure Key Vault (mounted via CSI driver "
            "rather than Kubernetes Secrets), enable pod-managed identities (workload identity) instead of "
            "service principal keys, use network policies to restrict pod-to-pod communication, and enable "
            "Defender for Containers for runtime threat detection. For compliance, enable Azure Policy for AKS "
            "to enforce standards like preventing privileged containers.\n\n"

            "Operational patterns: use namespaces to isolate teams or environments, implement resource quotas "
            "and limit ranges to prevent noisy neighbors, set pod disruption budgets (PDBs) for graceful "
            "upgrades, and use Velero for cluster backup and disaster recovery. AKS supports blue-green and "
            "canary deployments via Flagger or Argo Rollouts. For CI/CD, Azure DevOps pipelines or GitHub "
            "Actions can build images, push to ACR, and update Kubernetes manifests via Helm or Kustomize."
        ),
        "examples": [
            {
                "title": "AKS deployment with HPA and PDB",
                "code": (
                    "apiVersion: apps/v1\n"
                    "kind: Deployment\n"
                    "metadata:\n"
                    "  name: api-service\n"
                    "spec:\n"
                    "  replicas: 3\n"
                    "  selector:\n"
                    "    matchLabels: { app: api-service }\n"
                    "  template:\n"
                    "    spec:\n"
                    "      containers:\n"
                    "      - name: api\n"
                    "        image: myacr.azurecr.io/api:v1.2.3\n"
                    "        resources:\n"
                    "          requests: { cpu: 250m, memory: 512Mi }\n"
                    "          limits: { cpu: '1', memory: 1Gi }\n"
                    "---\n"
                    "apiVersion: autoscaling/v2\n"
                    "kind: HorizontalPodAutoscaler\n"
                    "metadata:\n"
                    "  name: api-service-hpa\n"
                    "spec:\n"
                    "  scaleTargetRef:\n"
                    "    apiVersion: apps/v1\n"
                    "    kind: Deployment\n"
                    "    name: api-service\n"
                    "  minReplicas: 3\n"
                    "  maxReplicas: 20\n"
                    "  metrics:\n"
                    "  - type: Resource\n"
                    "    resource:\n"
                    "      name: cpu\n"
                    "      target: { type: Utilization, averageUtilization: 70 }"
                ),
            },
            {
                "title": "Workload Identity for Key Vault access",
                "description": (
                    "1. Enable workload identity on the AKS cluster\n"
                    "2. Create an Azure managed identity\n"
                    "3. Create a Kubernetes ServiceAccount annotated with the managed identity's client ID\n"
                    "4. Create a federated identity credential linking the managed identity to the ServiceAccount\n"
                    "5. Grant the managed identity Key Vault Secrets User role on the Key Vault\n"
                    "6. Mount secrets via the CSI driver:\n"
                    "   - SecretProviderClass references the Key Vault\n"
                    "   - Pod mounts the CSI volume with the ServiceAccount\n"
                    "   - Secrets appear as files in the mounted volume"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Your AKS cluster has 50 microservices. During peak load, some pods are evicted due to resource pressure. How would you prevent this?",
                "hint": "Set appropriate resource requests and limits, use PriorityClasses to protect critical pods, enable cluster autoscaler, and use PDBs to prevent too many pods from being evicted simultaneously.",
            },
            {
                "question": "Design a zero-downtime deployment strategy for a stateful service (e.g., a database proxy) running on AKS.",
                "hint": "Use StatefulSet with rolling update strategy, set PDB minAvailable, configure readiness probes, and use preStop hooks with a sleep to allow in-flight requests to complete.",
            },
        ],
        "tags": ["azure", "aks", "kubernetes", "containers", "cloud-native"],
    },

    # ========== KAFKA (2 lessons) ==========
    {
        "category": "kafka",
        "title": "Kafka Fundamentals - Topics, Partitions, and Offsets",
        "slug": "kafka-fundamentals-topics-partitions-offsets",
        "difficulty": "intermediate",
        "order_index": 1,
        "content": (
            "Apache Kafka is a distributed event streaming platform designed for high-throughput, fault-tolerant, "
            "real-time data pipelines. At its core, Kafka is a distributed commit log: producers append messages "
            "to topics, and consumers read messages in order. Unlike traditional message queues, Kafka retains "
            "messages for a configurable duration (retention period, default 7 days) regardless of whether they "
            "have been consumed, enabling message replay and multiple consumer groups reading the same data.\n\n"

            "A topic is a logical channel for a category of messages (e.g., 'user-events', 'order-updates'). "
            "Each topic is divided into partitions - ordered, immutable sequences of messages. Partitions are "
            "the unit of parallelism: each partition is hosted on a single broker and can be consumed by exactly "
            "one consumer per consumer group. More partitions mean higher throughput (more consumers can read in "
            "parallel) but also more overhead (more file handles, more replication traffic, longer leader "
            "elections). A common starting point is 3-12 partitions per topic, scaling up as throughput demands.\n\n"

            "Each message within a partition has a unique offset - a monotonically increasing integer that "
            "serves as the message's position. Consumers track their progress by committing offsets. If a "
            "consumer restarts, it resumes from the last committed offset. Kafka offers two commit strategies: "
            "auto-commit (at regular intervals, risk of duplicates or loss) and manual commit (after processing, "
            "gives at-least-once semantics). The consumer stores committed offsets in the __consumer_offsets "
            "internal topic.\n\n"

            "Partitioning strategy determines which partition receives a message. By default, messages with a "
            "key are partitioned by hash(key) % numPartitions, ensuring all messages with the same key go to "
            "the same partition (and thus are ordered). Messages without a key use round-robin (or sticky "
            "partitioning in newer clients for better batching). Custom partitioners can implement business "
            "logic, such as routing by geographic region.\n\n"

            "Replication provides fault tolerance. Each partition has one leader and N-1 followers (replicas). "
            "Producers write to the leader, and followers replicate. The ISR (In-Sync Replicas) set contains "
            "followers that are caught up to the leader within replica.lag.time.max.ms. If the leader fails, "
            "a new leader is elected from the ISR. Setting min.insync.replicas=2 with acks=all ensures writes "
            "are acknowledged only when at least 2 replicas have the message, preventing data loss even if "
            "one broker fails."
        ),
        "examples": [
            {
                "title": "Producer with key-based partitioning (Java)",
                "code": (
                    "Properties props = new Properties();\n"
                    "props.put(\"bootstrap.servers\", \"broker1:9092,broker2:9092\");\n"
                    "props.put(\"key.serializer\", StringSerializer.class.getName());\n"
                    "props.put(\"value.serializer\", StringSerializer.class.getName());\n"
                    "props.put(\"acks\", \"all\");\n"
                    "props.put(\"retries\", 3);\n"
                    "props.put(\"enable.idempotence\", true);\n\n"
                    "KafkaProducer<String, String> producer = new KafkaProducer<>(props);\n\n"
                    "// Key = userId ensures all events for a user go to same partition\n"
                    "producer.send(new ProducerRecord<>(\n"
                    "    \"user-events\", userId, eventJson\n"
                    "), (metadata, exception) -> {\n"
                    "    if (exception != null) {\n"
                    "        log.error(\"Send failed\", exception);\n"
                    "    } else {\n"
                    "        log.info(\"Sent to partition {} offset {}\",\n"
                    "            metadata.partition(), metadata.offset());\n"
                    "    }\n"
                    "});"
                ),
            },
            {
                "title": "Consumer group with manual commit",
                "code": (
                    "Properties props = new Properties();\n"
                    "props.put(\"group.id\", \"order-processor\");\n"
                    "props.put(\"enable.auto.commit\", \"false\");\n"
                    "props.put(\"auto.offset.reset\", \"earliest\");\n\n"
                    "KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);\n"
                    "consumer.subscribe(List.of(\"orders\"));\n\n"
                    "while (true) {\n"
                    "    ConsumerRecords<String, String> records =\n"
                    "        consumer.poll(Duration.ofMillis(1000));\n"
                    "    for (ConsumerRecord<String, String> record : records) {\n"
                    "        processOrder(record.value());\n"
                    "    }\n"
                    "    consumer.commitSync(); // Commit after processing batch\n"
                    "}"
                ),
            },
        ],
        "exercises": [
            {
                "question": "You have a topic with 12 partitions and a consumer group with 15 consumers. What happens?",
                "hint": "Only 12 consumers will be assigned partitions (one each). The remaining 3 consumers will be idle. You cannot have more active consumers than partitions in a group.",
            },
            {
                "question": "Explain the difference between acks=0, acks=1, and acks=all. What are the trade-offs?",
                "hint": "acks=0: fire-and-forget (fastest, risk of loss). acks=1: leader acknowledges (moderate, loss if leader fails before replication). acks=all: all ISR replicas acknowledge (slowest, strongest durability).",
            },
        ],
        "tags": ["kafka", "streaming", "topics", "partitions", "consumer-groups"],
    },
    {
        "category": "kafka",
        "title": "Exactly-Once Semantics and Kafka Transactions",
        "slug": "exactly-once-semantics-kafka-transactions",
        "difficulty": "advanced",
        "order_index": 2,
        "content": (
            "Achieving exactly-once semantics (EOS) in a distributed streaming system is one of the hardest "
            "problems in distributed computing. Without special handling, systems provide either at-most-once "
            "(messages may be lost) or at-least-once (messages may be duplicated) delivery. Kafka's EOS "
            "support, introduced in version 0.11, provides exactly-once processing for consume-transform-produce "
            "patterns through two mechanisms: idempotent producers and transactions.\n\n"

            "An idempotent producer (enable.idempotence=true) ensures that retried sends do not produce "
            "duplicates within a single partition. The producer assigns a unique producer ID (PID) and a "
            "monotonically increasing sequence number to each message. The broker deduplicates messages by "
            "tracking the latest sequence number per PID per partition. If a message arrives with a sequence "
            "number already seen, it is silently discarded. This handles network retries transparently but only "
            "within a single producer session - if the producer restarts, it gets a new PID.\n\n"

            "Kafka transactions extend EOS across multiple partitions and consumer-producer pipelines. A "
            "transactional producer is configured with a unique transactional.id. The producer calls "
            "beginTransaction(), sends messages to multiple partitions, sends consumer offsets (via "
            "sendOffsetsToTransaction), and then either commitTransaction() or abortTransaction(). The broker's "
            "transaction coordinator manages a two-phase commit protocol: it writes transaction markers to "
            "all involved partitions, ensuring either all messages and offsets are visible or none are.\n\n"

            "On the consumer side, setting isolation.level=read_committed makes the consumer skip uncommitted "
            "messages (those within an ongoing or aborted transaction). This is essential: without it, consumers "
            "see messages from aborted transactions, breaking exactly-once semantics. The last stable offset "
            "(LSO) is the offset below which all transactions are resolved; consumers with read_committed never "
            "advance beyond the LSO.\n\n"

            "EOS comes with performance costs. Transactions add latency due to the two-phase commit protocol "
            "and the need to wait for transaction markers. The recommended pattern is to batch multiple messages "
            "within a single transaction to amortize the overhead. Transaction timeouts must be tuned: too short "
            "and slow consumers abort prematurely, too long and aborted transactions block the LSO, delaying "
            "read_committed consumers. For Kafka Streams, EOS is enabled with processing.guarantee=exactly_once_v2, "
            "which handles all the transactional plumbing internally."
        ),
        "examples": [
            {
                "title": "Transactional consume-transform-produce",
                "code": (
                    "Properties producerProps = new Properties();\n"
                    "producerProps.put(\"transactional.id\", \"order-enricher-1\");\n"
                    "producerProps.put(\"enable.idempotence\", true);\n"
                    "KafkaProducer<String, String> producer = new KafkaProducer<>(producerProps);\n"
                    "producer.initTransactions();\n\n"
                    "while (true) {\n"
                    "    ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));\n"
                    "    if (records.isEmpty()) continue;\n\n"
                    "    producer.beginTransaction();\n"
                    "    try {\n"
                    "        for (ConsumerRecord<String, String> record : records) {\n"
                    "            String enriched = enrich(record.value());\n"
                    "            producer.send(new ProducerRecord<>(\n"
                    "                \"enriched-orders\", record.key(), enriched));\n"
                    "        }\n"
                    "        // Commit consumer offsets within the same transaction\n"
                    "        producer.sendOffsetsToTransaction(\n"
                    "            currentOffsets(records), consumer.groupMetadata());\n"
                    "        producer.commitTransaction();\n"
                    "    } catch (Exception e) {\n"
                    "        producer.abortTransaction();\n"
                    "    }\n"
                    "}"
                ),
            },
            {
                "title": "Kafka Streams with exactly-once",
                "code": (
                    "Properties props = new Properties();\n"
                    "props.put(StreamsConfig.APPLICATION_ID_CONFIG, \"word-count\");\n"
                    "props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,\n"
                    "    StreamsConfig.EXACTLY_ONCE_V2);\n\n"
                    "StreamsBuilder builder = new StreamsBuilder();\n"
                    "builder.<String, String>stream(\"text-input\")\n"
                    "    .flatMapValues(value -> Arrays.asList(value.split(\"\\\\s+\")))\n"
                    "    .groupBy((key, word) -> word)\n"
                    "    .count(Materialized.as(\"word-counts\"))\n"
                    "    .toStream()\n"
                    "    .to(\"word-count-output\");\n\n"
                    "KafkaStreams streams = new KafkaStreams(builder.build(), props);\n"
                    "streams.start();"
                ),
            },
        ],
        "exercises": [
            {
                "question": "A transactional producer with transactional.id='txn-1' crashes and restarts. What happens to its in-flight transaction?",
                "hint": "On restart, initTransactions() fences the old producer instance (prevents zombie writes) and aborts any pending transaction from the previous instance. The new instance gets the same PID epoch incremented.",
            },
            {
                "question": "Explain why read_committed consumers can experience increased end-to-end latency compared to read_uncommitted consumers.",
                "hint": "read_committed consumers cannot read past the LSO. If a long-running transaction is open, the LSO is stuck, and all messages after it are buffered, even those from other committed transactions.",
            },
        ],
        "tags": ["kafka", "exactly-once", "transactions", "idempotent", "streaming"],
    },

    # ========== REDIS (1 lesson) ==========
    {
        "category": "redis",
        "title": "Redis Data Structures and Caching Patterns",
        "slug": "redis-data-structures-caching-patterns",
        "difficulty": "intermediate",
        "order_index": 1,
        "content": (
            "Redis is an in-memory data structure store used as a cache, message broker, and database. Its speed "
            "comes from keeping all data in memory and using a single-threaded event loop that avoids context "
            "switching and lock contention. Redis achieves 100K+ operations per second on a single node. Since "
            "Redis 6.0, I/O threading handles network reads/writes on multiple threads while command execution "
            "remains single-threaded, improving throughput for multi-core servers.\n\n"

            "Redis supports rich data structures beyond simple key-value pairs. Strings hold up to 512MB and "
            "support atomic increment/decrement (INCR, DECR) for counters. Lists are doubly-linked lists "
            "supporting push/pop from both ends (LPUSH, RPOP), ideal for queues and recent-items feeds. Sets "
            "are unordered collections of unique strings supporting set operations (SUNION, SINTER, SDIFF) - "
            "useful for tags, likes, and unique visitor tracking. Sorted Sets (ZSETs) maintain elements ordered "
            "by score, supporting range queries by rank or score (ZRANGEBYSCORE) - perfect for leaderboards, "
            "rate limiters, and priority queues.\n\n"

            "Hashes store field-value pairs under a single key (HSET, HGET, HGETALL), analogous to a row in a "
            "database table. They are memory-efficient for storing objects because Redis uses a compact "
            "encoding (ziplist) for small hashes. Streams (added in Redis 5.0) are an append-only log structure "
            "with consumer groups, designed for event streaming - they are Redis's answer to Kafka for simpler "
            "use cases. HyperLogLog provides probabilistic cardinality estimation (count unique elements) using "
            "only 12KB of memory regardless of the number of elements.\n\n"

            "Common caching patterns in Redis: Cache-Aside (application manages cache explicitly), Read-Through "
            "and Write-Through (cache layer handles DB interaction transparently), and Write-Behind (async DB "
            "updates). For distributed rate limiting, use a sorted set with timestamps as scores: ZADD the "
            "current timestamp, ZREMRANGEBYSCORE to remove old entries, and ZCARD to count recent requests. "
            "For distributed locks, use SET with NX and PX flags (SET key value NX PX 30000) or the Redlock "
            "algorithm for multi-node setups.\n\n"

            "Redis persistence options: RDB (point-in-time snapshots) provides compact backups but loses data "
            "since the last snapshot. AOF (Append Only File) logs every write command and can be replayed for "
            "recovery - choose appendfsync=everysec for a balance between durability and performance. In "
            "production, use both: RDB for backups and AOF for crash recovery. Redis Cluster provides horizontal "
            "scaling by sharding data across multiple nodes using hash slots (16384 total). Each key hashes to "
            "a slot, and each node owns a range of slots."
        ),
        "examples": [
            {
                "title": "Distributed rate limiter with sorted sets",
                "code": (
                    "-- Lua script for atomic rate limiting\n"
                    "-- KEYS[1] = rate limit key, ARGV[1] = window in ms,\n"
                    "-- ARGV[2] = max requests, ARGV[3] = current timestamp ms\n"
                    "local key = KEYS[1]\n"
                    "local window = tonumber(ARGV[1])\n"
                    "local limit = tonumber(ARGV[2])\n"
                    "local now = tonumber(ARGV[3])\n\n"
                    "-- Remove entries outside the window\n"
                    "redis.call('ZREMRANGEBYSCORE', key, 0, now - window)\n"
                    "local count = redis.call('ZCARD', key)\n\n"
                    "if count < limit then\n"
                    "    redis.call('ZADD', key, now, now .. '-' .. math.random())\n"
                    "    redis.call('PEXPIRE', key, window)\n"
                    "    return 1  -- allowed\n"
                    "end\n"
                    "return 0  -- rate limited"
                ),
            },
            {
                "title": "Session store with hash and TTL",
                "code": (
                    "# Store user session as a hash\n"
                    "HSET session:abc123 userId 42 role admin lastAccess 1700000000\n"
                    "EXPIRE session:abc123 1800  # 30-minute TTL\n\n"
                    "# Read session\n"
                    "HGETALL session:abc123\n"
                    "# => {\"userId\": \"42\", \"role\": \"admin\", \"lastAccess\": \"1700000000\"}\n\n"
                    "# Refresh TTL on access (sliding expiration)\n"
                    "EXPIRE session:abc123 1800"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Design a real-time leaderboard for a game with millions of players. Support: get top 10, get player rank, update score. What Redis data structure would you use?",
                "hint": "Use a Sorted Set. ZADD to update scores, ZREVRANGE 0 9 for top 10, ZREVRANK for player rank. All operations are O(log n). Use ZINCRBY for score increments.",
            },
            {
                "question": "Your Redis instance is using 90% of available memory. What strategies can you use to reduce memory usage without losing critical data?",
                "hint": "Set maxmemory-policy to allkeys-lru or volatile-lru. Use shorter key names. Compress values. Use hashes for small objects (ziplist encoding). Set TTLs aggressively. Move cold data to disk-backed storage.",
            },
        ],
        "tags": ["redis", "caching", "data-structures", "performance", "distributed-lock"],
    },

    # ========== LEADERSHIP (1 lesson) ==========
    {
        "category": "leadership",
        "title": "Driving Technical Strategy and the RFC Process",
        "slug": "driving-technical-strategy-rfc-process",
        "difficulty": "advanced",
        "order_index": 1,
        "content": (
            "At the Staff+ level, your impact comes not from writing more code but from shaping the technical "
            "direction of your organization. Technical strategy bridges business goals and engineering execution. "
            "It answers: given where the business wants to go in the next 1-3 years, what technical investments, "
            "migrations, and architectural decisions must we make now? A good technical strategy identifies the "
            "top 3-5 technical bets, explains the reasoning behind each, and defines measurable outcomes. It is "
            "a living document, revisited quarterly.\n\n"

            "The RFC (Request for Comments) process is the primary mechanism for driving alignment on significant "
            "technical decisions. An RFC is a written proposal that describes the problem, evaluates alternatives, "
            "proposes a solution, and invites feedback. Writing forces clarity: if you cannot clearly explain the "
            "problem and the trade-offs, you do not understand them well enough. An RFC should include: context "
            "and motivation, requirements and constraints, proposed design with diagrams, alternatives considered "
            "with pros/cons, migration plan, rollback strategy, and open questions.\n\n"

            "The RFC review process is as important as the document itself. Circulate the RFC to stakeholders "
            "across teams, not just your own. Set a review period (typically 1-2 weeks) and actively solicit "
            "feedback from people who will be affected. Address every comment: agree and update the RFC, disagree "
            "with reasoning, or mark as out of scope. The goal is not consensus but informed decision-making. "
            "Ultimately, the RFC author (or a designated decision maker) decides, with the understanding that "
            "disagreements are recorded and respected.\n\n"

            "Driving alignment is the most challenging leadership skill. People resist change for valid reasons: "
            "they have context you lack, they have competing priorities, or they disagree on the trade-offs. "
            "Effective alignment requires: one-on-one conversations before the group meeting (pre-wire key "
            "stakeholders), acknowledging trade-offs honestly (never pretend there are no downsides), showing "
            "empathy for the migration cost on other teams, offering to help with the transition, and being "
            "willing to modify your proposal based on feedback.\n\n"

            "Mentoring and sponsorship are distinct activities. Mentoring provides guidance: code reviews, "
            "architectural advice, career coaching. Sponsorship provides opportunity: recommending someone for "
            "a visible project, amplifying their work in leadership meetings, nominating them for promotion. "
            "As a Staff+ engineer, you should actively do both. Create leverage by raising the technical bar "
            "of your team through documentation, design patterns, and tooling that multiplies everyone's output. "
            "Your success is measured not by your personal output but by the engineering organization's "
            "improved capability."
        ),
        "examples": [
            {
                "title": "RFC template structure",
                "description": (
                    "# RFC: [Title]\n\n"
                    "**Status:** Draft | In Review | Accepted | Rejected | Superseded\n"
                    "**Author:** [Name]\n"
                    "**Reviewers:** [Names]\n"
                    "**Date:** [Date]\n\n"
                    "## Context and Problem Statement\n"
                    "What is the problem? Why does it matter now? What is the business impact?\n\n"
                    "## Requirements\n"
                    "- Must-haves (functional and non-functional)\n"
                    "- Nice-to-haves\n"
                    "- Out of scope\n\n"
                    "## Proposed Design\n"
                    "Architecture diagrams, data flow, API contracts, schema changes.\n\n"
                    "## Alternatives Considered\n"
                    "For each: description, pros, cons, reason for rejection.\n\n"
                    "## Migration Plan\n"
                    "Phases, backward compatibility, feature flags, rollback plan.\n\n"
                    "## Open Questions\n"
                    "Unresolved decisions that need input from reviewers."
                ),
            },
            {
                "title": "Technical strategy one-pager format",
                "description": (
                    "1. Current State: Where are we today? Key metrics and pain points.\n"
                    "2. Target State: Where do we need to be in 12 months? Tied to business goals.\n"
                    "3. Technical Bets (top 3-5):\n"
                    "   - Bet 1: Migrate from monolith to event-driven microservices\n"
                    "     - Why: 4x team growth requires independent deployability\n"
                    "     - Metric: Deploy frequency from weekly to daily per service\n"
                    "   - Bet 2: Adopt Infrastructure as Code (Terraform)\n"
                    "     - Why: Manual infra changes cause 60% of outages\n"
                    "     - Metric: Zero manual infrastructure changes in production\n"
                    "4. Sequencing: What order? What are the dependencies?\n"
                    "5. Investment: What teams and time are required?"
                ),
            },
        ],
        "exercises": [
            {
                "question": "Two teams disagree on whether to build a shared library or duplicate code. As a Staff engineer, how do you facilitate this decision?",
                "hint": "Understand both perspectives. A shared library creates a coupling point and requires versioning/governance. Duplication allows independent evolution. Evaluate: how often does the code change? How many teams use it? Is the API stable? Write an RFC with both options and trade-offs.",
            },
            {
                "question": "You believe the team should rewrite a critical service but your manager is skeptical. How do you build the case?",
                "hint": "Quantify the cost of the current system: incident frequency, time to add features, developer onboarding time. Propose a phased migration (strangler fig pattern) rather than a big-bang rewrite. Show a prototype. Get buy-in from other tech leads who are affected.",
            },
        ],
        "tags": ["leadership", "technical-strategy", "rfc", "mentoring", "staff-engineer"],
    },
]


# ======================================================================
# SYSTEM DESIGN PROBLEMS DATA
# ======================================================================

SYSTEM_DESIGN_PROBLEMS = [
    {
        "title": "Design Twitter/X",
        "slug": "design-twitter",
        "difficulty": "hard",
        "category": "web_scale",
        "description": "Design a social media platform like Twitter that supports posting short messages, following users, and viewing a personalized timeline. The system must handle hundreds of millions of users with high read-to-write ratios and deliver tweets in near real-time.",
        "requirements": {
            "functional": [
                "Users can post tweets (up to 280 characters with optional media)",
                "Users can follow and unfollow other users",
                "Users can view their home timeline (aggregated feed of followed users)",
                "Users can like, retweet, and reply to tweets",
                "Users can search tweets by keyword or hashtag",
                "Trending topics are computed and displayed",
                "Users receive notifications for mentions, likes, and retweets"
            ],
            "non_functional": [
                "Timeline generation should complete within 200ms",
                "System should support 500 million daily active users",
                "Availability of 99.99% (favor availability over consistency)",
                "New tweets should appear in followers' timelines within 5 seconds",
                "Support burst traffic during major events (10x normal load)"
            ]
        },
        "estimation_hints": {
            "users": "500M DAU, 200M tweets/day, average user follows 200 accounts",
            "storage": "Each tweet ~1KB text + metadata; media stored separately. ~200TB/year for tweet text, ~5PB/year for media",
            "bandwidth": "Read-heavy: ~100:1 read-to-write. ~500K timeline reads/sec at peak",
            "qps": "Write: ~2,300 tweets/sec average, 10K peak. Read: ~600K timeline fetches/sec peak"
        },
        "api_design": {
            "POST /api/v1/tweets": "Create a tweet with text body, optional media_ids array, and optional reply_to_id for threading",
            "GET /api/v1/timeline/home?cursor=&limit=": "Fetch the authenticated user's home timeline with cursor-based pagination",
            "GET /api/v1/timeline/user/:userId?cursor=&limit=": "Fetch a specific user's tweets in reverse chronological order",
            "POST /api/v1/users/:userId/follow": "Follow a user; returns updated follow status",
            "GET /api/v1/search?q=&type=tweets|users&cursor=": "Search tweets or users by keyword with pagination",
            "GET /api/v1/trends?region=": "Get trending topics for a given region"
        },
        "schema_design": {
            "tweets": "id (snowflake bigint PK), user_id (bigint FK), content (varchar 280), media_urls (jsonb), reply_to_id (bigint nullable), retweet_of_id (bigint nullable), like_count (int), retweet_count (int), created_at (timestamp). Partitioned by created_at.",
            "users": "id (bigint PK), username (varchar 50 unique), display_name (varchar 100), bio (text), follower_count (int), following_count (int), created_at (timestamp)",
            "follows": "follower_id (bigint), followee_id (bigint), created_at (timestamp). Composite PK (follower_id, followee_id). Index on followee_id for fan-out queries.",
            "timelines": "user_id (bigint), tweet_id (bigint), author_id (bigint), created_at (timestamp). Redis sorted set keyed by user_id, scored by timestamp. Stores pre-computed home timeline.",
            "likes": "user_id (bigint), tweet_id (bigint), created_at (timestamp). Composite PK."
        },
        "scaling_notes": "The core challenge is fan-out on write vs fan-out on read for timeline generation. For regular users, use fan-out on write: when a user tweets, push the tweet ID into each follower's pre-computed timeline cache (Redis sorted set). For celebrity users with millions of followers, use fan-out on read: their tweets are fetched and merged at read time to avoid overwhelming the write pipeline. This hybrid approach balances write amplification against read latency. Tweet storage uses a sharded SQL database partitioned by time, with recent tweets also cached in Redis. The search index uses Elasticsearch with inverted indices on tweet content. Media is stored in object storage (S3) behind a CDN. Use consistent hashing for cache distribution and implement circuit breakers between services to prevent cascade failures during traffic spikes.",
        "failure_modes": [
            "Timeline cache (Redis) failure: fall back to fan-out on read from the tweets table, accepting higher latency",
            "Celebrity tweet storm: a single viral tweet triggers millions of fan-out writes, potentially saturating the write pipeline",
            "Hot partition: trending hashtag concentrates reads on a single Elasticsearch shard",
            "Cascade failure: timeline service failure backs up requests into tweet service, causing system-wide degradation",
            "Split brain in cache cluster: followers see stale or inconsistent timelines across regions"
        ],
        "trade_offs": [
            "Consistency vs latency: eventual consistency in timelines (a follower might see a tweet a few seconds late) enables sub-200ms reads",
            "Fan-out on write vs read: write amplification for normal users trades storage and write throughput for fast reads; celebrities use the inverse",
            "Pre-computed vs on-demand timelines: storing materialized timelines in Redis costs ~500GB+ RAM but eliminates expensive join queries at read time",
            "Snowflake IDs vs auto-increment: Snowflake IDs are 64-bit, time-sortable, and shard-friendly but require a coordination service"
        ],
        "diagram_description": "Clients connect through a global CDN and load balancer to an API Gateway that routes to microservices. The Tweet Service handles write operations, storing tweets in a sharded PostgreSQL cluster and publishing events to Kafka. The Fan-out Service consumes tweet events, looks up followers from the Social Graph Service, and pushes tweet IDs into per-user timeline caches in a Redis cluster. The Timeline Service reads from Redis for normal users and merges celebrity tweets on the fly from the Tweet Cache. A Search Service backed by Elasticsearch indexes tweets asynchronously from Kafka. Media uploads go directly to S3 via pre-signed URLs, with a CDN serving media reads. A Trends Service processes tweet streams via Kafka Streams to compute trending topics. All services emit metrics to a monitoring stack and use circuit breakers for inter-service calls.",
        "order_index": 1
    },
    {
        "title": "Design Netflix",
        "slug": "design-netflix",
        "difficulty": "hard",
        "category": "data_intensive",
        "description": "Design a video streaming platform that serves millions of concurrent viewers with adaptive bitrate streaming. The system must handle massive content storage, efficient video delivery, and personalized recommendations while maintaining smooth playback.",
        "requirements": {
            "functional": [
                "Users can browse and search a catalog of movies and TV shows",
                "Users can stream video content with adaptive bitrate quality",
                "Users can pause, resume, and seek within a video",
                "Users receive personalized content recommendations",
                "Users can create profiles and manage watchlists",
                "Content can be uploaded and transcoded into multiple formats and resolutions"
            ],
            "non_functional": [
                "Video playback must start within 2 seconds",
                "Support 200 million subscribers with 10 million concurrent streams",
                "99.99% availability for the streaming path",
                "Buffer-free playback with adaptive quality switching",
                "Global coverage with low latency in all major regions"
            ]
        },
        "estimation_hints": {
            "users": "200M subscribers, 10M concurrent streams at peak, average session 1.5 hours",
            "storage": "~15,000 titles, each transcoded into ~1,200 files (resolution/bitrate combos). ~50PB total storage",
            "bandwidth": "Average stream 5 Mbps. Peak: 10M * 5Mbps = 50 Tbps outbound",
            "qps": "Catalog/search: ~100K req/sec. Stream manifest requests: ~10M/sec during peak. Play/pause events: ~1M/sec"
        },
        "api_design": {
            "GET /api/v1/catalog?genre=&sort=&cursor=": "Browse content catalog with filters, sorting, and pagination",
            "GET /api/v1/search?q=&type=": "Search titles, actors, directors by keyword",
            "GET /api/v1/titles/:titleId/manifest": "Get streaming manifest (DASH/HLS) with available bitrates and CDN URLs",
            "POST /api/v1/playback/start": "Record playback start event with title, profile, device info; returns resume position",
            "POST /api/v1/playback/heartbeat": "Periodic playback position update for resume and analytics",
            "GET /api/v1/recommendations/:profileId": "Get personalized content recommendations for a profile"
        },
        "schema_design": {
            "titles": "id (uuid PK), type (enum: movie, series), name (varchar), description (text), release_year (int), genres (jsonb), cast (jsonb), rating (varchar), duration_minutes (int), poster_url (varchar), created_at (timestamp)",
            "video_files": "id (uuid PK), title_id (uuid FK), resolution (varchar), bitrate_kbps (int), codec (varchar), file_size_bytes (bigint), s3_key (varchar), cdn_url (varchar), segment_duration_sec (int)",
            "profiles": "id (uuid PK), account_id (uuid FK), name (varchar), avatar_url (varchar), maturity_level (varchar), language (varchar)",
            "watch_history": "profile_id (uuid), title_id (uuid), position_seconds (int), completed (boolean), last_watched (timestamp). PK (profile_id, title_id). Used for resume and recommendations.",
            "viewing_activity": "id (bigint PK), profile_id (uuid), title_id (uuid), event_type (enum), device (varchar), bitrate (int), buffer_events (int), timestamp (timestamp). Append-only, partitioned by day."
        },
        "scaling_notes": "The biggest challenge is delivering 50+ Tbps of video bandwidth globally. Netflix uses Open Connect, a custom CDN with appliances placed inside ISP networks. Popular content is pre-positioned on edge servers close to viewers, eliminating backbone traversal. Video files are pre-transcoded into hundreds of bitrate-resolution combinations using per-title encoding optimization that tailors the encoding ladder to each title's complexity. The catalog and recommendation services are backed by Cassandra for high write throughput and EVCache (memcached-based) for low-latency reads. Microservices communicate via gRPC with Zuul as the API gateway. Chaos engineering (Chaos Monkey, Chaos Kong) continuously validates resilience. Regional failover uses active-active deployment across three AWS regions with Cassandra's multi-datacenter replication.",
        "failure_modes": [
            "CDN edge server failure: redirect viewers to the next closest edge node with slightly higher latency",
            "Transcoding pipeline failure: new content cannot be prepared for streaming; implement retries and dead-letter queues",
            "Recommendation service timeout: fall back to popularity-based and genre-based recommendations",
            "Regional AWS outage: Zuul reroutes traffic to healthy regions; Cassandra serves from replica datacenter",
            "Thundering herd on new release: pre-warm CDN caches and use staggered rollout by region"
        ],
        "trade_offs": [
            "Storage cost vs encoding quality: encoding each title into 1,200 variants costs ~$10K in compute per title but reduces rebuffering by 30%",
            "Edge caching vs origin: placing content on ISP edge appliances costs hardware but saves 90% of backbone bandwidth",
            "Eventual consistency in viewing history: a user switching devices might miss the last 30 seconds of progress but the system avoids cross-region synchronous writes",
            "Microservice complexity vs monolith: hundreds of microservices increase operational overhead but enable independent scaling and deployment"
        ],
        "diagram_description": "Users connect through DNS-based routing to the nearest Open Connect edge server or CDN node for video delivery. Non-video API requests go through a cloud load balancer to Zuul API Gateway, which routes to backend microservices. The Catalog Service serves content metadata from EVCache (backed by Cassandra). The Recommendation Service runs ML models against user viewing history stored in Cassandra. The Playback Service generates streaming manifests pointing to the optimal CDN nodes. Video upload triggers an asynchronous transcoding pipeline that produces multiple bitrate variants and pushes them to S3 origin storage, from which the CDN pulls and caches content. A Control Plane manages CDN content placement based on popularity predictions. All services publish events to Kafka for real-time analytics, A/B test evaluation, and feeding the recommendation model training pipeline.",
        "order_index": 2
    },
    {
        "title": "Design Uber",
        "slug": "design-uber",
        "difficulty": "hard",
        "category": "real_time",
        "description": "Design a ride-sharing platform that matches riders with nearby drivers in real-time. The system must handle location tracking, dynamic pricing, route optimization, and payment processing at massive scale across hundreds of cities.",
        "requirements": {
            "functional": [
                "Riders can request a ride specifying pickup and drop-off locations",
                "System matches riders with the nearest available drivers in real-time",
                "Drivers receive ride requests and can accept or decline",
                "Real-time GPS tracking of driver and ride progress",
                "Dynamic pricing (surge) based on supply and demand",
                "Fare estimation before ride confirmation",
                "Payment processing at ride completion"
            ],
            "non_functional": [
                "Ride matching should complete within 10 seconds",
                "Location updates processed within 1 second",
                "Support 20 million rides per day across 700+ cities",
                "99.99% availability for ride matching and dispatch",
                "Accurate ETA predictions within 2 minutes of actual arrival"
            ]
        },
        "estimation_hints": {
            "users": "100M monthly active riders, 5M active drivers, 20M rides/day",
            "storage": "Driver location updates: 5M drivers * 1 update/4 sec = 1.25M updates/sec. Trip records: ~20M/day * 5KB = 100GB/day",
            "bandwidth": "Location updates: 1.25M/sec * 200 bytes = 250MB/sec inbound. Map tile serving: ~500K tiles/sec",
            "qps": "Location updates: 1.25M/sec. Ride requests: ~230/sec average, 1,000/sec peak. ETA calculations: ~500K/sec"
        },
        "api_design": {
            "POST /api/v1/rides/request": "Request a ride with pickup lat/lng, dropoff lat/lng, ride type (UberX, Pool, etc.), payment method",
            "PUT /api/v1/drivers/:driverId/location": "Update driver location with lat, lng, heading, speed. Called every 4 seconds by driver app",
            "POST /api/v1/rides/:rideId/accept": "Driver accepts a ride request; triggers rider notification and route calculation",
            "GET /api/v1/rides/:rideId/track": "WebSocket endpoint for real-time ride tracking (driver location, ETA updates)",
            "GET /api/v1/rides/estimate?pickup_lat=&pickup_lng=&dropoff_lat=&dropoff_lng=": "Get fare estimate and ETA for a route",
            "POST /api/v1/rides/:rideId/complete": "Complete a ride, trigger fare calculation and payment"
        },
        "schema_design": {
            "rides": "id (uuid PK), rider_id (uuid FK), driver_id (uuid FK), status (enum: requested, matched, in_progress, completed, cancelled), pickup_location (point), dropoff_location (point), fare_cents (int), surge_multiplier (decimal), distance_miles (decimal), duration_minutes (int), requested_at (timestamp), completed_at (timestamp)",
            "drivers": "id (uuid PK), name (varchar), vehicle_type (varchar), license_plate (varchar), status (enum: offline, available, en_route, on_trip), current_location (point), heading (float), rating (decimal), city_id (int FK)",
            "driver_locations": "driver_id (uuid), location (point), heading (float), speed (float), timestamp (timestamp). Written to a geospatial index (Google S2 or H3) in Redis for fast proximity queries. Time-series data stored in Cassandra.",
            "payments": "id (uuid PK), ride_id (uuid FK), rider_id (uuid FK), driver_id (uuid FK), amount_cents (int), currency (varchar), status (enum: pending, charged, refunded), payment_method_id (uuid), processed_at (timestamp)",
            "surge_zones": "city_id (int), h3_cell (varchar), surge_multiplier (decimal), demand_count (int), supply_count (int), computed_at (timestamp). Updated every 30 seconds per H3 hexagonal cell."
        },
        "scaling_notes": "The critical path is real-time driver matching, which requires sub-second geospatial queries across millions of active drivers. Driver locations are indexed using H3 hexagonal cells in an in-memory geospatial store (Redis with geospatial commands or a custom ringpop-based service). When a ride request arrives, the dispatch service queries the geospatial index for available drivers within expanding radius rings. Each city runs as an independent cell with its own dispatch service instance, enabling horizontal scaling by geography. The supply-demand balance is computed per H3 cell every 30 seconds for surge pricing. Location updates flow through Kafka to decouple the ingestion rate from processing. Trip data is stored in a sharded MySQL cluster (Schemaless - Uber's custom storage on MySQL). ETAs use a machine learning model trained on historical trip data combined with real-time traffic from driver GPS streams.",
        "failure_modes": [
            "Geospatial index failure: no driver matching possible; queue ride requests and retry with exponential backoff",
            "GPS signal loss: driver location goes stale; mark driver unavailable after 30 seconds of no updates",
            "Payment gateway timeout: complete the ride but defer payment processing to an async retry queue",
            "Surge computation lag: stale pricing during rapid demand changes leads to driver-rider mismatch",
            "Regional datacenter failure: reroute to secondary region; in-flight rides continue on cached state"
        ],
        "trade_offs": [
            "Precision vs speed in matching: searching a wider radius finds better matches but increases response time; Uber uses expanding rings to balance both",
            "Consistency vs availability for ride state: a ride must not be double-assigned, so ride matching uses a strongly consistent store even at the cost of higher latency",
            "Real-time vs batch surge pricing: real-time surge is more responsive but noisier; 30-second windows smooth out transient spikes",
            "Cell-based architecture: isolates failures to a single city but complicates cross-city rides and global analytics"
        ],
        "diagram_description": "The mobile apps connect through a global load balancer to an API Gateway that routes requests to domain services. The Ride Request Service receives ride requests and publishes them to the Dispatch Service, which queries the Location Service's geospatial index (H3-indexed Redis) for nearby available drivers. When a match is found, the Dispatch Service notifies the driver via a persistent WebSocket connection managed by the Real-Time Communication Service. Driver location updates stream through Kafka into the Location Service's geospatial index and into Cassandra for historical storage. The Pricing Service computes surge multipliers from supply-demand data aggregated per H3 cell. The ETA Service uses a routing engine with real-time traffic data. The Payment Service processes fares asynchronously via a payment gateway. The Trip Service stores completed ride data in sharded MySQL. All services are deployed per-city cell for isolation.",
        "order_index": 3
    },
    {
        "title": "Design WhatsApp",
        "slug": "design-whatsapp",
        "difficulty": "hard",
        "category": "real_time",
        "description": "Design an end-to-end encrypted messaging platform supporting one-on-one and group chats, media sharing, and message delivery status. The system must support 2 billion users with reliable message delivery and minimal latency.",
        "requirements": {
            "functional": [
                "Send and receive text messages in one-on-one and group conversations",
                "Share images, videos, documents, and voice messages",
                "Display message delivery status (sent, delivered, read)",
                "Support group chats with up to 1,024 members",
                "End-to-end encryption for all messages",
                "Offline message delivery when recipient comes online",
                "Last-seen and online status indicators"
            ],
            "non_functional": [
                "Message delivery latency under 200ms for online users",
                "Support 2 billion registered users, 500 million DAU",
                "Handle 100 billion messages per day",
                "Messages must be reliably delivered (at-least-once, deduplicated by client)",
                "99.999% uptime for the messaging path"
            ]
        },
        "estimation_hints": {
            "users": "2B registered, 500M DAU, average user sends 40 messages/day",
            "storage": "100B messages/day * 100 bytes avg = 10TB/day text. Media: ~50TB/day. Messages stored until delivered (not permanently server-side).",
            "bandwidth": "Inbound: 100B msgs * 100 bytes / 86400 = ~115 MB/sec text. Media: ~5 Gbps inbound",
            "qps": "Message sends: ~1.15M/sec average, 5M/sec peak. Connection management: 500M persistent connections"
        },
        "api_design": {
            "WS /api/v1/connect": "Establish persistent WebSocket connection for real-time message delivery. Authenticates via token in handshake.",
            "POST /api/v1/messages/send": "Send a message (text or media reference) to a user or group. Returns message_id and server timestamp.",
            "GET /api/v1/messages/sync?last_seen_id=": "Sync missed messages since last connection. Returns ordered batch of pending messages.",
            "POST /api/v1/messages/:messageId/ack": "Acknowledge message receipt (delivered/read). Server relays status to sender.",
            "POST /api/v1/media/upload": "Upload encrypted media file, returns media_id and CDN URL for referencing in messages",
            "GET /api/v1/groups/:groupId/members": "List group members with roles (admin, member)"
        },
        "schema_design": {
            "messages": "id (bigint PK, snowflake), sender_id (bigint), conversation_id (bigint), type (enum: text, image, video, audio, document), encrypted_content (blob), media_url (varchar nullable), timestamp (bigint epoch_ms), status (enum: sent, delivered, read). Partitioned by conversation_id. TTL-based cleanup after delivery.",
            "conversations": "id (bigint PK), type (enum: direct, group), participant_ids (set of bigint), created_at (timestamp). For direct chats, a composite key of sorted user IDs ensures uniqueness.",
            "user_sessions": "user_id (bigint PK), device_id (varchar), server_id (varchar - which chat server holds the WebSocket), connected_at (timestamp), last_heartbeat (timestamp). Stored in Redis for fast routing.",
            "offline_queue": "user_id (bigint), message_id (bigint), conversation_id (bigint), enqueued_at (timestamp). Per-user queue in Cassandra, drained when user reconnects.",
            "groups": "id (bigint PK), name (varchar), admin_ids (set of bigint), member_ids (set of bigint), created_at (timestamp). Max 1,024 members."
        },
        "scaling_notes": "The primary scaling challenge is maintaining 500 million concurrent WebSocket connections. Each chat server handles ~1 million connections on dedicated high-memory machines. A session registry in Redis maps each online user to their chat server. When user A sends a message to user B, the gateway looks up B's server in Redis and routes the message there. For offline users, messages are queued in Cassandra and drained on reconnection. Group messages use fan-out on write: the server sends a copy to each member's chat server. Cassandra is used for message storage with partition keys on conversation_id for locality. Media files are encrypted client-side, uploaded to S3, and the CDN URL is sent in the message payload. The encryption key is transmitted inside the end-to-end encrypted message, so the server never has access to media content. Erlang/BEAM is used for the chat servers due to its lightweight process model (millions of concurrent processes per node).",
        "failure_modes": [
            "Chat server crash: 1 million users disconnect; clients auto-reconnect to another server and drain their offline queues",
            "Redis session registry failure: message routing fails; fall back to broadcasting to all servers in the user's region",
            "Cassandra offline queue data loss: messages are lost for offline users; use replication factor 3 and quorum writes",
            "Group message fan-out overload: a message to a 1,024-member group generates 1,024 deliveries simultaneously",
            "Network partition between datacenters: messages in-flight during partition may be duplicated; clients deduplicate by message_id"
        ],
        "trade_offs": [
            "At-least-once vs exactly-once delivery: server uses at-least-once delivery for reliability; clients deduplicate using message IDs to achieve effective exactly-once",
            "Server-side storage vs ephemeral: messages are deleted from the server after delivery to reduce storage costs and improve privacy, but complicates multi-device sync",
            "WebSocket vs long polling: WebSockets provide lower latency but are harder to load-balance and consume more server resources per connection",
            "Erlang vs JVM: Erlang's actor model handles millions of concurrent connections naturally but has a smaller ecosystem and hiring pool"
        ],
        "diagram_description": "Mobile clients establish persistent WebSocket connections through regional load balancers to a pool of Chat Servers (Erlang nodes), each handling ~1M connections. A Redis-based Session Registry maps each online user to their assigned Chat Server. The Message Router reads from the Session Registry to deliver messages: for online recipients it forwards to the target Chat Server, for offline recipients it enqueues in the Offline Queue (Cassandra). When a user reconnects, the Chat Server drains their offline queue. Media files are encrypted client-side and uploaded to S3 via a Media Service, with CDN URLs embedded in messages. Group messages are fanned out by the Chat Server to each member's assigned server. A Presence Service tracks online/last-seen status. All events flow to Kafka for analytics. End-to-end encryption keys are exchanged via the Signal Protocol during session setup.",
        "order_index": 4
    },
    {
        "title": "Design YouTube",
        "slug": "design-youtube",
        "difficulty": "hard",
        "category": "data_intensive",
        "description": "Design a video sharing platform where users upload, transcode, store, and stream user-generated video content. The system must handle billions of video views per day with efficient content delivery and a recommendation engine that drives engagement.",
        "requirements": {
            "functional": [
                "Users can upload videos with title, description, and tags",
                "Videos are transcoded into multiple resolutions and formats",
                "Users can stream videos with adaptive bitrate playback",
                "Users can search videos by title, description, tags, and captions",
                "Users can like, comment on, and share videos",
                "Personalized video recommendations on the home page",
                "Channel subscriptions and notification system"
            ],
            "non_functional": [
                "Support 2 billion monthly active users and 1 billion hours of video watched daily",
                "Video upload to availability within 15 minutes for standard content",
                "99.9% availability for video streaming",
                "Playback start time under 2 seconds",
                "Global low-latency delivery via edge caching"
            ]
        },
        "estimation_hints": {
            "users": "2B MAU, 500M DAU. 500 hours of video uploaded every minute. 1B hours watched/day.",
            "storage": "~1 exabyte total. Each video stored in ~20 resolution/codec variants. Average raw upload: 500MB, becomes 3GB after transcoding.",
            "bandwidth": "Peak streaming: ~100 Tbps outbound. Upload: ~500 Gbps inbound.",
            "qps": "Video metadata reads: ~5M/sec. Search: ~500K/sec. Upload initiation: ~6K/sec. Comment writes: ~50K/sec."
        },
        "api_design": {
            "POST /api/v1/videos/upload/init": "Initialize a resumable upload session; returns upload_url and upload_id for chunked upload",
            "PUT /api/v1/videos/upload/:uploadId": "Upload a video chunk (resumable). Client sends chunks with byte range headers.",
            "GET /api/v1/videos/:videoId": "Get video metadata (title, description, view count, like count, channel info, available qualities)",
            "GET /api/v1/videos/:videoId/stream/:quality": "Get HLS/DASH manifest for a specific quality; CDN-backed segment URLs",
            "GET /api/v1/search?q=&filters=&cursor=": "Search videos with text query, filters (duration, upload date, type), and pagination",
            "GET /api/v1/feed/recommendations?cursor=": "Get personalized video recommendations for the home feed"
        },
        "schema_design": {
            "videos": "id (bigint PK), channel_id (bigint FK), title (varchar 200), description (text), tags (jsonb), status (enum: processing, active, removed), duration_seconds (int), view_count (bigint), like_count (bigint), upload_timestamp (timestamp), published_at (timestamp)",
            "video_files": "video_id (bigint FK), resolution (varchar), codec (varchar), bitrate_kbps (int), file_size_bytes (bigint), storage_path (varchar), segment_count (int). One row per transcoded variant.",
            "channels": "id (bigint PK), owner_user_id (bigint FK), name (varchar), description (text), subscriber_count (bigint), created_at (timestamp)",
            "comments": "id (bigint PK), video_id (bigint FK), user_id (bigint FK), parent_comment_id (bigint nullable), text (text), like_count (int), created_at (timestamp). Indexed by (video_id, created_at).",
            "watch_history": "user_id (bigint), video_id (bigint), watch_duration_seconds (int), total_duration_seconds (int), watched_at (timestamp). Used for recommendations. Stored in Bigtable/Cassandra partitioned by user_id."
        },
        "scaling_notes": "The transcoding pipeline is the most compute-intensive component. Videos are split into segments, transcoded in parallel across a fleet of GPU-accelerated workers managed by a job scheduler. Each segment is transcoded into 20+ resolution/codec combinations. Completed segments are assembled and pushed to origin storage. The CDN serves the vast majority of views from edge caches, with popularity-based pre-warming. View counts use approximate counters (Redis HyperLogLog for unique views, batched counter updates to avoid write hotspots on popular videos). The recommendation system runs on a deep learning model trained on watch history, using a two-stage approach: candidate generation (retrieve ~1,000 candidates from a large corpus) and ranking (score and order candidates by predicted watch time). Search uses an inverted index with video title, description, auto-generated captions, and tags.",
        "failure_modes": [
            "Transcoding worker failure: job scheduler reassigns the segment to another worker; idempotent processing ensures no duplicate output",
            "CDN cache miss storm: a viral video not yet cached at edge triggers thundering herd to origin; use request coalescing at the CDN layer",
            "View count inconsistency: batched counter updates mean displayed counts lag reality by up to 60 seconds",
            "Search index lag: newly uploaded videos may not appear in search for several minutes during indexing",
            "Comment spam flood: rate limiting and ML-based spam detection may lag, briefly surfacing spam comments"
        ],
        "trade_offs": [
            "Transcoding breadth vs storage cost: more transcoded variants improve playback quality across devices but multiply storage costs 20x per video",
            "Approximate vs exact view counts: approximate counting (batch updates, HyperLogLog) prevents write hotspots but delays accurate counts by up to a minute",
            "Recommendation relevance vs diversity: optimizing purely for predicted watch time creates filter bubbles; diversity injection reduces engagement slightly but improves user satisfaction long-term",
            "Resumable uploads vs simple uploads: resumable uploads add client complexity but are essential for large files over unreliable connections"
        ],
        "diagram_description": "Users upload videos through an API Gateway to the Upload Service, which stores raw files in blob storage and enqueues transcoding jobs. A distributed Transcoding Pipeline (managed by a job scheduler) splits videos into segments, transcodes each in parallel across GPU workers, and writes output segments to origin blob storage. A Metadata Service backed by a sharded SQL database stores video information. The CDN pulls and caches video segments from origin storage, serving most views from edge. Clients request streaming manifests from the Playback Service, which returns CDN-backed HLS/DASH URLs. A Search Service indexes video metadata and auto-generated captions in Elasticsearch. The Recommendation Service generates personalized feeds using a two-stage ML pipeline (candidate retrieval from an embedding index, ranking with a deep model). View events flow through Kafka to the Analytics pipeline and feed the recommendation model training loop.",
        "order_index": 5
    },
    {
        "title": "Design Google Search",
        "slug": "design-google-search",
        "difficulty": "hard",
        "category": "web_scale",
        "description": "Design a web search engine that crawls, indexes, and ranks billions of web pages. The system must return relevant results for any text query within milliseconds, handling tens of thousands of queries per second.",
        "requirements": {
            "functional": [
                "Users can search the web using text queries and receive ranked results",
                "Results include title, snippet, and URL with relevance ranking",
                "Support advanced search operators (site:, filetype:, exact phrase)",
                "Auto-complete and spelling suggestions as the user types",
                "Web crawler continuously discovers and indexes new and updated pages",
                "Image, video, and news search capabilities"
            ],
            "non_functional": [
                "Search results returned within 500ms for 99th percentile",
                "Handle 100,000 queries per second",
                "Index of 100+ billion web pages",
                "Freshness: popular pages re-crawled within hours",
                "High relevance: top-10 results should satisfy 80%+ of queries"
            ]
        },
        "estimation_hints": {
            "users": "5B searches/day, ~100K QPS average, 500K QPS peak",
            "storage": "100B pages * 2MB avg = 200PB raw. Compressed index: ~50PB. Document store: ~100PB",
            "bandwidth": "Crawling: ~50 Gbps outbound. Serving: ~500 Gbps outbound for results pages",
            "qps": "Search queries: 100K/sec. Autocomplete: 300K/sec. Crawler fetch: 50K pages/sec"
        },
        "api_design": {
            "GET /api/v1/search?q=&start=&num=&safe=": "Execute a search query with pagination (start offset, num results per page), safe search filter",
            "GET /api/v1/suggest?q=&lang=": "Get autocomplete suggestions as user types; returns ranked list of query completions",
            "GET /api/v1/search/images?q=&size=&color=": "Image search with filters for size, color, type",
            "GET /api/v1/cache/:pageId": "Retrieve cached version of a crawled page",
            "POST /api/v1/index/submit": "Submit a URL for crawling (sitemap submission)"
        },
        "schema_design": {
            "documents": "doc_id (bigint PK), url (varchar unique), domain (varchar), title (text), content_hash (varchar), crawled_at (timestamp), page_rank (float), language (varchar), content_type (varchar). Stored in Bigtable.",
            "inverted_index": "term (varchar), posting_list (compressed list of doc_id, term_frequency, positions). Sharded by term hash. Each posting entry includes position data for phrase queries. Stored in custom SSTable format.",
            "page_rank_graph": "source_doc_id (bigint), target_doc_id (bigint), anchor_text (varchar). The link graph used for PageRank computation. Stored in a distributed graph database.",
            "crawl_queue": "url (varchar), domain (varchar), priority (float), last_crawled (timestamp), crawl_frequency (interval). Priority queue sharded by domain for politeness."
        },
        "scaling_notes": "The search index is the core data structure: an inverted index mapping every term to the sorted list of documents containing it, with term frequencies and positions for ranking. The index is sharded across thousands of machines, with each shard holding a subset of the document space. A query is broadcast to all index shards in parallel, each returns its top-K results, and a merger combines and re-ranks them. PageRank is computed offline via iterative MapReduce over the link graph. Real-time ranking combines PageRank with hundreds of signals (term frequency, freshness, user engagement, page quality) using a machine learning model. The crawler uses a URL frontier with per-domain rate limiting for politeness, prioritizing pages by PageRank and freshness requirements. Autocomplete uses a trie-based index of popular query prefixes with frequency counts, served from in-memory caches at the edge.",
        "failure_modes": [
            "Index shard failure: queries degrade gracefully by returning results from remaining shards with slightly reduced recall",
            "Crawler overload on a domain: per-domain rate limiting prevents this, but misconfiguration could lead to the domain blocking the crawler IP range",
            "Stale index: if the indexing pipeline lags, results may miss recent pages; freshness signals in ranking partially mitigate this",
            "Autocomplete cache corruption: serve stale suggestions from a secondary cache while rebuilding",
            "Spam pages polluting results: adversarial SEO can temporarily boost spam pages until the spam classifier catches up"
        ],
        "trade_offs": [
            "Index freshness vs completeness: re-crawling frequently keeps results fresh but limits total crawl coverage; priority-based scheduling balances both",
            "Ranking quality vs latency: more ranking signals and re-ranking passes improve relevance but increase tail latency; a two-phase approach (fast initial retrieval, ML re-ranking on top-1000) balances both",
            "Inverted index vs forward index: inverted indices are fast for keyword lookup but expensive for document-at-a-time scoring; a hybrid approach is used",
            "Centralized vs distributed crawling: distributed crawlers scale better but make duplicate detection and politeness enforcement harder"
        ],
        "diagram_description": "The Web Crawler runs on a distributed fleet, fetching pages from the internet based on a priority-managed URL Frontier that enforces per-domain politeness. Crawled pages flow through a Content Processing Pipeline that extracts text, detects language, deduplicates, and computes content quality scores. The Indexer builds and maintains a distributed Inverted Index sharded across thousands of machines. When a user submits a query, the Query Parser normalizes and expands it, then broadcasts it to all Index Shards in parallel. Each shard returns its local top-K candidates. The Merger aggregates results, and the ML Ranker re-scores the top candidates using PageRank, freshness, quality, and engagement signals. The Snippet Generator extracts relevant text fragments. Autocomplete queries hit an in-memory Trie Cache. A separate offline pipeline computes PageRank over the Link Graph using iterative MapReduce. Spell correction uses a noisy channel model with n-gram language models.",
        "order_index": 6
    },
    {
        "title": "Design Amazon",
        "slug": "design-amazon-ecommerce",
        "difficulty": "hard",
        "category": "web_scale",
        "description": "Design an e-commerce platform that handles product catalog management, search, shopping cart, checkout, order fulfillment, and seller marketplace operations. The system must support millions of concurrent shoppers with strong consistency for inventory and payments.",
        "requirements": {
            "functional": [
                "Users can browse and search products with filters (price, category, rating, Prime eligibility)",
                "Users can add items to a persistent shopping cart",
                "Users can complete checkout with address selection, payment, and order placement",
                "Sellers can list products with pricing, inventory, and descriptions",
                "Real-time inventory tracking across warehouses",
                "Order tracking from placement to delivery",
                "Product reviews and ratings"
            ],
            "non_functional": [
                "Product search returns results within 200ms",
                "Cart and checkout must be strongly consistent (no overselling)",
                "Support 300 million active customer accounts",
                "Handle 50x traffic spikes during Prime Day / Black Friday",
                "99.99% availability for the shopping cart and checkout path"
            ]
        },
        "estimation_hints": {
            "users": "300M active accounts, 50M DAU, 3M concurrent users at peak",
            "storage": "500M+ products. Product catalog: ~5TB. Order history: ~100TB. User data: ~20TB",
            "bandwidth": "Product pages: ~2M/sec at peak. Search: ~500K/sec. Checkout: ~50K orders/sec peak (Prime Day)",
            "qps": "Product detail: 2M/sec. Search: 500K/sec. Add to cart: 200K/sec. Place order: 50K/sec peak"
        },
        "api_design": {
            "GET /api/v1/products/search?q=&category=&price_min=&price_max=&sort=&cursor=": "Search products with filters and pagination",
            "GET /api/v1/products/:productId": "Get product details including price, inventory status, reviews summary, seller info",
            "POST /api/v1/cart/items": "Add item to cart with product_id and quantity; returns updated cart",
            "POST /api/v1/orders/checkout": "Place an order from cart items; validates inventory, reserves stock, processes payment atomically",
            "GET /api/v1/orders/:orderId/tracking": "Get order tracking status with shipment details and estimated delivery",
            "POST /api/v1/products/:productId/reviews": "Submit a product review with rating (1-5) and text"
        },
        "schema_design": {
            "products": "id (bigint PK), seller_id (bigint FK), title (varchar 500), description (text), category_path (ltree), price_cents (int), currency (varchar 3), images (jsonb), attributes (jsonb), rating_avg (decimal), review_count (int), status (enum: active, inactive), created_at (timestamp)",
            "inventory": "product_id (bigint), warehouse_id (int), quantity_available (int), quantity_reserved (int), last_updated (timestamp). PK (product_id, warehouse_id). Uses optimistic locking (version column) to prevent overselling.",
            "orders": "id (bigint PK), customer_id (bigint FK), status (enum: placed, payment_confirmed, shipped, delivered, returned), total_cents (int), shipping_address_id (bigint FK), placed_at (timestamp), delivered_at (timestamp nullable)",
            "order_items": "order_id (bigint FK), product_id (bigint FK), seller_id (bigint FK), quantity (int), price_cents (int), fulfillment_status (enum). PK (order_id, product_id).",
            "carts": "user_id (bigint PK), items (jsonb array of {product_id, quantity, added_at}), updated_at (timestamp). Stored in DynamoDB for fast access."
        },
        "scaling_notes": "The checkout flow is the most critical path and requires strong consistency for inventory. A two-phase approach is used: first, inventory is reserved (decrement available, increment reserved) using optimistic concurrency control, then payment is processed, and finally the reservation is confirmed. If payment fails, the reservation is released. This ensures no overselling while keeping the critical section short. Product search uses Elasticsearch with denormalized product data, updated asynchronously from the product catalog database. The shopping cart is stored in DynamoDB for low-latency access and automatic scaling. During peak events, the system pre-scales: additional capacity is provisioned, popular product pages are pre-cached, and non-essential features (recommendations, reviews) can be degraded to protect the buy path. Product catalog uses a CQRS pattern: writes go to the normalized relational store, reads come from denormalized caches and search indices.",
        "failure_modes": [
            "Payment gateway timeout during checkout: hold inventory reservation for 10 minutes while retrying; release if payment ultimately fails",
            "Inventory service overload during flash sale: rate-limit concurrent checkouts per product; show 'limited availability' messaging",
            "Search index lag: newly listed products or price changes may not appear for minutes; cache-aside pattern for popular products mitigates this",
            "Cart service failure: degrade to session-based cart stored in client cookies; merge with persistent cart on recovery",
            "Warehouse system failure: route fulfillment to alternative warehouses; increase estimated delivery time"
        ],
        "trade_offs": [
            "Strong consistency for inventory vs throughput: optimistic locking prevents overselling but limits checkout throughput per product; hot products may need inventory pre-split across virtual partitions",
            "Denormalized search index vs storage: duplicating product data in Elasticsearch increases storage but enables sub-200ms faceted search across 500M+ products",
            "Shopping cart in DynamoDB vs SQL: DynamoDB provides automatic scaling and single-digit millisecond latency but limits query flexibility",
            "CQRS complexity: separating read and write models adds eventual consistency lag but enables independent scaling of the catalog write path and the high-throughput read path"
        ],
        "diagram_description": "Users interact through a CDN and API Gateway that routes to microservices. The Product Catalog Service manages product data in a sharded PostgreSQL cluster, publishing changes to Kafka. The Search Service consumes catalog events and maintains an Elasticsearch index. The Cart Service stores shopping carts in DynamoDB. During checkout, the Order Service orchestrates a saga: it calls the Inventory Service to reserve stock (optimistic locking on the inventory table), then the Payment Service to charge the customer, then confirms the order. If any step fails, compensating transactions release resources. The Fulfillment Service assigns orders to the nearest warehouse with available stock. An event-driven architecture via Kafka connects services for order status updates, inventory sync, and analytics. Recommendations are served by an ML-based Recommendation Service reading from a feature store.",
        "order_index": 7
    },
    {
        "title": "Design Instagram",
        "slug": "design-instagram",
        "difficulty": "medium",
        "category": "web_scale",
        "description": "Design a photo and video sharing social network where users post content, follow other users, and interact through likes and comments. The system must deliver a fast, personalized feed and handle high media upload and serving throughput.",
        "requirements": {
            "functional": [
                "Users can upload photos and short videos with captions and filters",
                "Users can follow other users and view a personalized feed",
                "Users can like, comment on, and save posts",
                "Users can view stories (ephemeral 24-hour content)",
                "Hashtag and location-based content discovery",
                "Direct messaging between users"
            ],
            "non_functional": [
                "Feed generation within 200ms",
                "Photo upload and display within 5 seconds",
                "Support 2 billion monthly active users",
                "Media serving via CDN with 99.9% cache hit rate for popular content",
                "Eventual consistency acceptable for likes/comments counts"
            ]
        },
        "estimation_hints": {
            "users": "2B MAU, 500M DAU, 100M photos/videos uploaded daily",
            "storage": "Average photo: 2MB (stored in 4 resolutions). 100M * 2MB * 4 = 800TB/day new media. Total: ~200PB",
            "bandwidth": "Media serving: ~30 Tbps peak. Upload: ~2 Tbps inbound",
            "qps": "Feed reads: 1M/sec. Photo uploads: ~1,200/sec. Likes: ~500K/sec. Comments: ~50K/sec"
        },
        "api_design": {
            "POST /api/v1/posts": "Create a post with media files, caption, location, and tags. Returns post_id.",
            "GET /api/v1/feed?cursor=": "Get personalized home feed with cursor-based pagination",
            "POST /api/v1/posts/:postId/like": "Like or unlike a post (toggle). Returns updated like state.",
            "GET /api/v1/users/:userId/posts?cursor=": "Get a user's profile grid with cursor pagination",
            "GET /api/v1/explore?cursor=": "Get explore/discover feed based on interests and trending content",
            "POST /api/v1/stories": "Upload a story (auto-expires after 24 hours)"
        },
        "schema_design": {
            "posts": "id (bigint PK), user_id (bigint FK), media_urls (jsonb), caption (text), location (point nullable), hashtags (jsonb), like_count (bigint), comment_count (int), created_at (timestamp)",
            "follows": "follower_id (bigint), followee_id (bigint), created_at (timestamp). Composite PK. Indexed both directions.",
            "likes": "user_id (bigint), post_id (bigint), created_at (timestamp). Composite PK. Counter cache updated asynchronously.",
            "stories": "id (bigint PK), user_id (bigint FK), media_url (varchar), type (enum: photo, video), viewers (set of bigint), created_at (timestamp), expires_at (timestamp). TTL-based auto-deletion.",
            "feed_cache": "user_id (bigint), post_ids (sorted set scored by timestamp). Redis sorted set. Pre-computed for active users."
        },
        "scaling_notes": "Instagram's architecture mirrors parts of Twitter's feed system but with heavier media. Feed generation uses a hybrid fan-out approach: posts from accounts with under 10K followers are pushed to all followers' feed caches; posts from larger accounts are pulled at read time. Photo processing runs asynchronously: uploads go to a staging area, a pipeline generates multiple resolution thumbnails (150px, 320px, 640px, 1080px), applies any filters server-side, and pushes results to S3 behind a CDN. Like counts use Redis atomic counters with periodic persistence to the database. The explore/discover feed is powered by an ML model that scores content based on user interests, post engagement velocity, and content understanding (image classification, hashtag analysis). Stories use a separate fast path with TTL-based storage in Cassandra, avoiding the main post pipeline entirely.",
        "failure_modes": [
            "Feed cache miss: regenerate feed on the fly by querying followed users' recent posts; slower but functional",
            "Photo processing pipeline backlog: uploads succeed but display is delayed; show a processing placeholder",
            "Like counter drift: Redis counter and database diverge during high throughput; periodic reconciliation job corrects drift",
            "CDN origin overload for viral content: implement request coalescing and stale-while-revalidate caching",
            "Story expiration job lag: some stories may remain visible slightly past 24 hours during high load"
        ],
        "trade_offs": [
            "Pre-computed vs on-demand feeds: pre-computation uses significant Redis memory (~2KB per user * 500M users) but delivers sub-200ms feed loads",
            "Multiple image resolutions vs single: storing 4 resolutions per photo quadruples storage but reduces bandwidth by serving the right size for each device",
            "Eventual consistency for engagement counts: users may see slightly stale like/comment counts but the system avoids write hotspots on popular posts",
            "Separate stories pipeline: duplicates some infrastructure but allows stories to have different latency and retention characteristics"
        ],
        "diagram_description": "Users upload media through an API Gateway to the Post Service, which stores metadata in sharded PostgreSQL and queues media processing jobs. The Media Pipeline generates thumbnails in multiple resolutions and stores them in S3. A CDN serves media globally with high cache hit rates. The Feed Service uses a hybrid fan-out model: the Fan-out Worker pushes post IDs to followers' Redis feed caches for normal users, while celebrity posts are merged at read time. The Timeline Service reads from Redis feed caches and enriches posts with metadata. The Explore Service runs an ML ranking model to generate discovery feeds. Stories go through a separate lightweight pipeline with Cassandra storage and automatic TTL expiration. Engagement events (likes, comments) flow through Kafka for async counter updates, notifications, and analytics.",
        "order_index": 8
    },
    {
        "title": "Design Slack",
        "slug": "design-slack",
        "difficulty": "medium",
        "category": "real_time",
        "description": "Design a team communication platform with channels, direct messages, file sharing, and real-time message delivery. The system must support thousands of concurrent users per workspace with features like threading, reactions, and search across message history.",
        "requirements": {
            "functional": [
                "Users can send messages in channels (public/private) and direct messages",
                "Real-time message delivery to all channel members",
                "Message threading and reactions (emoji responses)",
                "File and image sharing within messages",
                "Full-text search across all accessible messages",
                "User presence (online/away/do not disturb) indicators"
            ],
            "non_functional": [
                "Message delivery latency under 100ms within a workspace",
                "Support 10 million daily active users across 500K workspaces",
                "Full message history with search across years of data",
                "99.99% uptime for the messaging path",
                "Support workspaces with up to 100,000 members"
            ]
        },
        "estimation_hints": {
            "users": "10M DAU across 500K workspaces. Average user sends 50 messages/day. Average workspace: 200 members.",
            "storage": "500M messages/day * 500 bytes = 250GB/day text. File uploads: ~5TB/day. Total message archive: ~500TB",
            "bandwidth": "Message delivery: ~50MB/sec. File serving: ~5 Gbps. WebSocket connections: ~10M concurrent.",
            "qps": "Message sends: ~6K/sec. Message reads: ~100K/sec. Search: ~10K/sec. Presence updates: ~50K/sec."
        },
        "api_design": {
            "WS /api/v1/rtm.connect": "Establish real-time messaging WebSocket connection for the workspace",
            "POST /api/v1/chat.postMessage": "Send a message to a channel or DM with text, attachments, and optional thread_ts for threading",
            "GET /api/v1/conversations.history?channel=&cursor=&limit=": "Fetch message history for a channel with cursor-based pagination",
            "GET /api/v1/search.messages?query=&sort=&cursor=": "Full-text search across messages the user has access to",
            "POST /api/v1/reactions.add": "Add an emoji reaction to a message (channel, timestamp, emoji name)",
            "POST /api/v1/files.upload": "Upload a file to a channel with optional initial comment"
        },
        "schema_design": {
            "messages": "workspace_id (bigint), channel_id (bigint), ts (varchar - unique message timestamp as ID), user_id (bigint), text (text), attachments (jsonb), thread_ts (varchar nullable), reply_count (int), reactions (jsonb), edited_at (timestamp nullable). PK (channel_id, ts). Partitioned by workspace_id.",
            "channels": "id (bigint PK), workspace_id (bigint FK), name (varchar), type (enum: public, private, dm, group_dm), topic (text), member_count (int), created_at (timestamp)",
            "channel_members": "channel_id (bigint), user_id (bigint), role (enum: member, admin, owner), last_read_ts (varchar), notification_pref (varchar), joined_at (timestamp). PK (channel_id, user_id).",
            "workspaces": "id (bigint PK), name (varchar), domain (varchar unique), plan (varchar), member_count (int), created_at (timestamp)",
            "user_presence": "user_id (bigint PK), workspace_id (bigint), status (enum: active, away, dnd), status_text (varchar), last_activity (timestamp). Stored in Redis with TTL for automatic away detection."
        },
        "scaling_notes": "Slack's architecture is organized by workspace, enabling natural sharding. Each workspace's data (messages, channels, members) is stored on a dedicated database shard or shard group. This provides strong data locality - most operations involve a single workspace and hit a single shard. Real-time message delivery uses a pub/sub system (Redis Pub/Sub or a custom message broker) where each channel is a topic. When a user connects via WebSocket, the gateway server subscribes to all the user's channels. For large channels with thousands of members, message delivery is fanned out through a dedicated broadcast service that batches WebSocket writes. Search is powered by Elasticsearch with per-workspace indices, enabling fast full-text search within a workspace's boundaries. File uploads go to S3 with virus scanning in the processing pipeline. Presence is managed in Redis with heartbeat-based liveness detection and batch presence updates to reduce WebSocket traffic.",
        "failure_modes": [
            "WebSocket gateway failure: clients reconnect and replay missed messages using the last_read_ts cursor",
            "Database shard failure for a workspace: the entire workspace is unavailable; failover to read replica promotes it to primary",
            "Search index lag: recent messages may not appear in search for 30-60 seconds during indexing delay",
            "File upload virus scan backlog: files are quarantined and unavailable for download until scan completes",
            "Presence service failure: users appear as 'away' until presence heartbeats resume; functional but confusing"
        ],
        "trade_offs": [
            "Workspace-based sharding vs global sharding: workspace sharding gives excellent locality but complicates Slack Connect (cross-workspace channels)",
            "Message timestamps as IDs vs auto-increment: timestamps provide natural ordering and are human-readable but require sub-millisecond precision to avoid collisions",
            "Persistent WebSocket vs HTTP polling: WebSockets provide real-time delivery but require sticky sessions and complicate load balancing",
            "Per-workspace search indices vs global: per-workspace indices keep search fast and isolated but multiply the number of indices Elasticsearch manages"
        ],
        "diagram_description": "Users connect through a load balancer to WebSocket Gateway servers that maintain persistent connections. When a message is posted, the API server writes it to the workspace's database shard and publishes the message to a Redis Pub/Sub channel. The Gateway servers subscribe to relevant channels and push messages to connected clients. For large channels, a Fan-out Service handles batch delivery to avoid overloading a single gateway. File uploads go through a File Service to S3 with an asynchronous virus scanning pipeline. An Elasticsearch cluster indexes messages per workspace for search. A Presence Service tracks user status in Redis with heartbeat TTLs. The Notification Service sends push notifications and emails for offline users. Channel membership and workspace data live on the same shard as messages for locality.",
        "order_index": 9
    },
    {
        "title": "Design Spotify",
        "slug": "design-spotify",
        "difficulty": "medium",
        "category": "data_intensive",
        "description": "Design a music streaming platform with a vast catalog, personalized playlists, offline downloads, and social sharing. The system must deliver seamless audio playback with adaptive quality and power discovery through recommendation algorithms.",
        "requirements": {
            "functional": [
                "Users can search and browse a catalog of songs, albums, and artists",
                "Users can stream music with adaptive audio quality",
                "Users can create, edit, and share playlists",
                "Personalized recommendations (Discover Weekly, Daily Mix, radio)",
                "Offline download for premium subscribers",
                "Social features: follow friends, share tracks, collaborative playlists"
            ],
            "non_functional": [
                "Playback start within 500ms of pressing play",
                "Support 500 million users and 50 million concurrent streams",
                "Catalog of 100 million tracks",
                "Seamless gapless playback between tracks",
                "99.9% availability for the streaming path"
            ]
        },
        "estimation_hints": {
            "users": "500M total users, 200M premium subscribers, 50M concurrent streams at peak",
            "storage": "100M tracks * 5 quality levels * 5MB avg = 2.5PB audio files. Metadata: ~500GB. User data: ~10TB",
            "bandwidth": "50M concurrent * 160kbps avg = 8 Tbps outbound at peak. Metadata API: ~50 Gbps.",
            "qps": "Track plays: ~50M/sec peak. Search: ~200K/sec. Playlist reads: ~500K/sec. Metadata lookups: ~2M/sec."
        },
        "api_design": {
            "GET /api/v1/tracks/:trackId/stream?quality=": "Get audio stream URL for a track at specified quality (low/normal/high/very_high). Returns CDN URL with auth token.",
            "GET /api/v1/search?q=&type=track,album,artist&limit=": "Search across tracks, albums, and artists with type filtering",
            "GET /api/v1/playlists/:playlistId/tracks?offset=&limit=": "Get tracks in a playlist with pagination",
            "POST /api/v1/playlists/:playlistId/tracks": "Add tracks to a playlist by track_id list",
            "GET /api/v1/recommendations/daily-mix/:mixId": "Get a personalized daily mix playlist",
            "GET /api/v1/browse/new-releases?country=&limit=": "Get new releases filtered by country"
        },
        "schema_design": {
            "tracks": "id (bigint PK), title (varchar), artist_ids (bigint array), album_id (bigint FK), duration_ms (int), explicit (boolean), popularity (int 0-100), isrc (varchar), preview_url (varchar), available_markets (varchar array)",
            "albums": "id (bigint PK), title (varchar), artist_ids (bigint array), release_date (date), total_tracks (int), label (varchar), cover_art_urls (jsonb - multiple sizes)",
            "playlists": "id (bigint PK), owner_id (bigint FK), name (varchar), description (text), public (boolean), collaborative (boolean), follower_count (int), snapshot_id (varchar - for conflict detection), created_at (timestamp)",
            "playlist_tracks": "playlist_id (bigint), track_id (bigint), added_by (bigint FK), added_at (timestamp), position (int). PK (playlist_id, position).",
            "listening_history": "user_id (bigint), track_id (bigint), context (varchar - playlist/album/radio), played_at (timestamp), duration_played_ms (int). Partitioned by user_id and month. Core data for recommendations."
        },
        "scaling_notes": "Audio files are pre-encoded in multiple quality levels (96kbps, 160kbps, 320kbps OGG Vorbis for free tier; up to 320kbps for premium) and cached aggressively on CDN edge nodes. The long tail of less popular tracks may not be cached at the edge, so a tiered caching strategy is used: L1 edge cache for top 1% of tracks (which account for 80% of plays), L2 regional cache for the next 19%, and origin for the remaining 80% of tracks. The recommendation engine uses collaborative filtering (users who listened to X also listened to Y) combined with content-based analysis (audio features, genre, tempo) and natural language processing on music reviews and articles. Spotify's Discover Weekly uses a matrix factorization model on the user-track interaction matrix. The playlist service uses Cassandra for high write throughput (millions of playlist edits per day). The search index uses Elasticsearch with custom analyzers for handling multilingual artist and track names.",
        "failure_modes": [
            "CDN cache miss for a popular track: origin server serves directly while cache is populated; higher latency for that play",
            "Recommendation service failure: fall back to curated editorial playlists and popularity-based suggestions",
            "Playlist service failure: playlists are read-only from cache; edits are queued and applied when the service recovers",
            "Audio quality degradation: adaptive bitrate reduces quality on poor connections rather than buffering",
            "Rights management failure: a track becomes unavailable in certain markets; fail gracefully by skipping and playing the next track"
        ],
        "trade_offs": [
            "Multiple audio encodings vs single: storing 5 quality variants per track multiplies storage 5x but enables adaptive streaming and instant quality switching",
            "Collaborative filtering vs content-based recommendations: collaborative filtering captures taste patterns but suffers from cold-start for new users; content-based analysis works for new tracks but misses social trends",
            "Gapless playback vs simplicity: gapless playback requires the client to pre-buffer the next track and handle crossfades, adding client complexity",
            "Cassandra for playlists vs SQL: Cassandra handles high write throughput for millions of concurrent playlist edits but makes complex queries (search within playlists) harder"
        ],
        "diagram_description": "Clients connect through a CDN and API Gateway. The Playback Service resolves track IDs to CDN-backed audio file URLs with short-lived authentication tokens. Audio files are served from a three-tier CDN: edge caches (top tracks), regional caches (mid-popularity), and S3 origin (long tail). The Catalog Service manages track, album, and artist metadata in a PostgreSQL cluster with heavy caching in Memcached. The Playlist Service stores playlists in Cassandra for high write throughput. The Search Service uses Elasticsearch with custom multilingual analyzers. The Recommendation Engine runs batch (Spark) and real-time (Kafka Streams) ML pipelines, producing personalized playlists stored in Cassandra. Listening events stream through Kafka to feed the recommendation pipeline, analytics, royalty calculation, and the popularity index. A Rights Service enforces geographic availability based on licensing data.",
        "order_index": 10
    },
    {
        "title": "Design Rate Limiter",
        "slug": "design-rate-limiter",
        "difficulty": "medium",
        "category": "infrastructure",
        "description": "Design a distributed rate limiting service that controls the number of requests a client can make within a time window. The system must work across multiple API gateway instances with minimal latency overhead and support different rate limiting strategies.",
        "requirements": {
            "functional": [
                "Limit requests per client (by API key, user ID, or IP address) within configurable time windows",
                "Support multiple algorithms: fixed window, sliding window, token bucket, leaky bucket",
                "Return rate limit headers (remaining, reset time) in every response",
                "Support different limits per endpoint, plan tier, and client",
                "Allow configuration changes without service restart",
                "Provide a dashboard for monitoring rate limit usage and violations"
            ],
            "non_functional": [
                "Decision latency under 1ms at the 99th percentile",
                "Consistent enforcement across all API gateway instances (minimal over-allowance)",
                "Support 1 million rate limit decisions per second",
                "Graceful degradation: if the rate limiter is down, default to allowing requests",
                "Minimal memory footprint per tracked client"
            ]
        },
        "estimation_hints": {
            "users": "100K API clients, each with multiple endpoints. 1M rate limit checks/sec.",
            "storage": "Per-client counter: ~100 bytes. 100K clients * 10 endpoints = 1M entries * 100 bytes = 100MB in-memory",
            "bandwidth": "Rate limit check: ~200 bytes request + 100 bytes response. 1M/sec * 300 bytes = 300MB/sec",
            "qps": "1M rate limit checks/sec. Config reads: ~100/sec. Dashboard queries: ~10/sec."
        },
        "api_design": {
            "POST /api/v1/ratelimit/check": "Check if a request should be allowed. Input: client_id, endpoint, request metadata. Returns: allowed (boolean), remaining, limit, reset_at",
            "GET /api/v1/ratelimit/config/:clientId": "Get rate limit configuration for a client (limits per endpoint, algorithm, tier)",
            "PUT /api/v1/ratelimit/config/:clientId": "Update rate limit configuration for a client",
            "GET /api/v1/ratelimit/stats/:clientId": "Get usage statistics: current counts, violations in the last hour/day",
            "POST /api/v1/ratelimit/override": "Temporarily override a client's limits (for incident response or special events)"
        },
        "schema_design": {
            "rate_configs": "client_id (varchar), endpoint_pattern (varchar), algorithm (enum: fixed_window, sliding_window, token_bucket), max_requests (int), window_seconds (int), burst_size (int nullable), tier (varchar). PK (client_id, endpoint_pattern). Stored in SQL, cached in each gateway instance.",
            "rate_counters": "key (varchar - composite of client_id:endpoint:window_start), count (int), expires_at (timestamp). Stored in Redis with TTL matching the window size. For sliding window: Redis sorted set with request timestamps.",
            "violation_log": "id (bigint PK), client_id (varchar), endpoint (varchar), timestamp (timestamp), request_count (int), limit (int). Append-only log for analytics. Stored in time-series DB or Kafka topic."
        },
        "scaling_notes": "The rate limiter must operate on the critical path of every API request, so latency is paramount. The primary decision engine uses Redis with Lua scripts to make atomic check-and-increment operations. For the fixed window algorithm, a simple INCR with EXPIRE achieves O(1) time. The sliding window log algorithm uses a sorted set per client-endpoint pair, adding each request timestamp and counting entries within the window - this is more accurate but costs O(log N) per operation. The token bucket algorithm stores remaining tokens and last refill time, computing available tokens on each check. To reduce Redis round trips, API gateways maintain local counters that sync with Redis periodically (every 100ms). This introduces a small window where limits can be slightly exceeded (by the number of gateway instances times the sync interval's traffic) but reduces Redis load by 10x. Configuration is cached locally with a 30-second TTL, refreshed from a SQL configuration store.",
        "failure_modes": [
            "Redis failure: fall back to local in-memory counters per gateway instance; limits are enforced per-instance rather than globally, allowing up to N times the limit where N is the number of instances",
            "Clock skew between instances: sliding window calculations may be inaccurate; use Redis server time rather than local clocks",
            "Hot key (single client sending massive traffic): Redis hash slots may become hot; use client-side caching to absorb most checks locally",
            "Configuration propagation delay: a config change may take up to 30 seconds to reach all gateway instances"
        ],
        "trade_offs": [
            "Accuracy vs latency: local counters with periodic sync to Redis reduce latency to near-zero but allow brief over-allowance during sync windows",
            "Fixed window vs sliding window: fixed windows are simpler and cheaper (single counter vs sorted set) but allow burst traffic at window boundaries",
            "Token bucket vs sliding window: token bucket naturally handles burst (up to bucket size) while sliding window strictly enforces the rate; token bucket is better for APIs that see legitimate traffic spikes",
            "Fail-open vs fail-closed: defaulting to allow on rate limiter failure protects availability but exposes the backend to overload; fail-closed protects the backend but may block legitimate traffic"
        ],
        "diagram_description": "API requests arrive at a load balancer and are distributed across multiple API Gateway instances. Each gateway has a local Rate Limit Module that first checks an in-memory cache for the client's configuration and current counter. For the first check or when the local cache is expired, the module makes an atomic Lua-scripted call to a Redis cluster to check and increment the counter. Redis stores counters with TTL-based expiration matching the rate window. The Rate Limit Configuration Service stores and manages per-client and per-endpoint limits in PostgreSQL, pushing updates to each gateway's local cache via a pub/sub notification channel. A Monitoring Service reads violation events from a Kafka topic and powers a dashboard showing usage patterns and rate limit breaches. The gateway injects X-RateLimit-Remaining and X-RateLimit-Reset headers into every response.",
        "order_index": 11
    },
    {
        "title": "Design URL Shortener",
        "slug": "design-url-shortener",
        "difficulty": "medium",
        "category": "infrastructure",
        "description": "Design a URL shortening service like bit.ly that generates short aliases for long URLs, redirects users, and tracks click analytics. The system must handle high redirect throughput with low latency and provide real-time click statistics.",
        "requirements": {
            "functional": [
                "Users can submit a long URL and receive a shortened URL",
                "Shortened URLs redirect to the original URL",
                "Users can optionally specify a custom short alias",
                "Click analytics: total clicks, clicks by country, referrer, device, and time",
                "URLs can have optional expiration dates",
                "Users can view and manage their shortened URLs"
            ],
            "non_functional": [
                "Redirect latency under 10ms (99th percentile)",
                "Support 1 billion redirects per day",
                "Shortened URLs should be as short as possible (7 characters)",
                "99.99% availability for the redirect path",
                "Analytics available within 5 seconds of a click"
            ]
        },
        "estimation_hints": {
            "users": "10M registered users. 10M new URLs/day. 1B redirects/day (100:1 read-to-write).",
            "storage": "Each URL mapping: ~500 bytes. 10M/day * 365 * 5 years = 18B records * 500 bytes = 9TB total. Analytics: ~50TB/year",
            "bandwidth": "Redirects: ~12K/sec avg, 50K/sec peak. Each redirect: 500 bytes request, 300 bytes response (301 + Location header).",
            "qps": "Redirects: 12K/sec avg, 50K/sec peak. URL creation: ~120/sec. Analytics reads: ~1K/sec."
        },
        "api_design": {
            "POST /api/v1/urls/shorten": "Create a shortened URL. Input: long_url, custom_alias (optional), expires_at (optional). Returns: short_url, created_at",
            "GET /:shortCode": "Redirect to the original URL (301/302). Records click event asynchronously.",
            "GET /api/v1/urls/:shortCode/stats": "Get click analytics: total_clicks, clicks_by_day, top_countries, top_referrers, top_devices",
            "GET /api/v1/urls?cursor=&limit=": "List the authenticated user's shortened URLs with pagination",
            "DELETE /api/v1/urls/:shortCode": "Delete a shortened URL (returns 404 on future redirects)"
        },
        "schema_design": {
            "urls": "id (bigint PK), short_code (varchar 10, unique indexed), original_url (text), user_id (bigint FK nullable), created_at (timestamp), expires_at (timestamp nullable), click_count (bigint default 0)",
            "clicks": "id (bigint PK), short_code (varchar), clicked_at (timestamp), ip_address (varchar), country (varchar), city (varchar), referrer (varchar), user_agent (varchar), device_type (varchar). Append-only, partitioned by day. Written asynchronously via Kafka.",
            "click_aggregates": "short_code (varchar), date (date), country (varchar), device_type (varchar), click_count (int). PK (short_code, date, country, device_type). Pre-aggregated by a stream processor for fast analytics queries."
        },
        "scaling_notes": "The redirect path is read-heavy (100:1 ratio) and latency-critical. The short_code to URL mapping is cached in a distributed Redis cache with the entire hot working set (~10GB) fitting in memory. Cache misses fall through to a sharded MySQL or DynamoDB lookup. Short code generation uses a base62 encoding of a distributed counter (Snowflake-style ID generator) to ensure uniqueness without coordination. The 7-character base62 code supports 62^7 = 3.5 trillion unique URLs. Click tracking is entirely asynchronous: the redirect handler fires a Kafka event and returns the 301 immediately. A stream processing pipeline (Kafka Streams or Flink) consumes click events, enriches them with GeoIP data, and writes to both the raw clicks table (for detailed queries) and pre-aggregated counters (for dashboard queries). Expired URLs are cleaned up by a background job that scans for past-due expiration timestamps.",
        "failure_modes": [
            "Redis cache failure: redirects fall through to the database; latency increases from ~1ms to ~10ms but service remains functional",
            "Kafka click event queue backup: click analytics lag behind but redirects are unaffected since analytics is async",
            "Counter service failure: URL creation fails; implement a fallback to random code generation with collision checking",
            "Hot short code (viral link): a single URL may receive millions of clicks; Redis handles this well but monitor for hot-key issues on specific Redis slots"
        ],
        "trade_offs": [
            "Sequential counter vs random codes: sequential counters are collision-free but predictable (users can enumerate URLs); random codes prevent enumeration but require collision checking",
            "301 (permanent) vs 302 (temporary) redirect: 301 lets browsers cache the redirect (reducing load) but makes click tracking incomplete since cached redirects bypass the server",
            "Real-time vs batch analytics: real-time stream processing provides 5-second analytics freshness but costs more in infrastructure than hourly batch jobs",
            "Short code length: 6 characters support 56B URLs but are easier to guess; 7 characters support 3.5T URLs with better security"
        ],
        "diagram_description": "Users submit URLs through an API Gateway to the URL Service, which generates a unique short code using a distributed counter, stores the mapping in a sharded database, and populates the Redis cache. When a short URL is accessed, the Redirect Service looks up the short code in Redis (cache hit) or the database (cache miss) and returns a 301 redirect. Before responding, it publishes a click event to Kafka asynchronously. A Click Processing Pipeline (Kafka Streams) consumes click events, enriches them with GeoIP and User-Agent parsing, and writes to both a raw Clicks table (partitioned by day in Cassandra or TimescaleDB) and pre-aggregated counters for the analytics dashboard. The Analytics API reads from the aggregated counters for fast dashboard queries and from the raw table for custom date range queries. A background Expiration Worker periodically removes expired URLs from the database and cache.",
        "order_index": 12
    },
    {
        "title": "Design Pastebin",
        "slug": "design-pastebin",
        "difficulty": "medium",
        "category": "infrastructure",
        "description": "Design a text sharing service where users can store and share plain text or code snippets via generated URLs. The system must handle high read traffic for popular pastes, support syntax highlighting, and optionally allow paste expiration and password protection.",
        "requirements": {
            "functional": [
                "Users can create pastes with text content and optional title",
                "Each paste gets a unique short URL for sharing",
                "Syntax highlighting for popular programming languages",
                "Optional paste expiration (10 minutes, 1 hour, 1 day, 1 week, never)",
                "Optional password protection for private pastes",
                "View raw paste content or formatted HTML"
            ],
            "non_functional": [
                "Paste retrieval under 50ms",
                "Support 5 million pastes created per day",
                "Handle 50 million paste reads per day",
                "99.9% availability",
                "Maximum paste size: 10MB"
            ]
        },
        "estimation_hints": {
            "users": "5M pastes/day, 50M reads/day (10:1 read-to-write). 1M registered users.",
            "storage": "Average paste: 10KB. 5M/day * 365 * 3 years = 5.5B pastes * 10KB = 55TB. With replication: ~165TB",
            "bandwidth": "Reads: ~600/sec avg. 600/sec * 10KB = 6MB/sec. Writes: ~60/sec avg.",
            "qps": "Paste reads: 600/sec avg, 2K/sec peak. Paste creates: 60/sec avg. Raw content fetches: 200/sec."
        },
        "api_design": {
            "POST /api/v1/pastes": "Create a paste. Input: content (text), title (optional), language (optional), expiration (optional), password (optional). Returns: paste_id, url, created_at",
            "GET /api/v1/pastes/:pasteId": "Get paste metadata and highlighted content. Requires password header if paste is protected.",
            "GET /api/v1/pastes/:pasteId/raw": "Get raw text content of a paste",
            "GET /api/v1/pastes/recent?limit=": "List recent public pastes (for the homepage feed)",
            "DELETE /api/v1/pastes/:pasteId": "Delete a paste (owner only)"
        },
        "schema_design": {
            "pastes": "id (varchar 8, PK - base62 encoded), user_id (bigint FK nullable), title (varchar 200 nullable), language (varchar 50 nullable), content_key (varchar - S3/blob key for the actual content), size_bytes (int), password_hash (varchar nullable), created_at (timestamp), expires_at (timestamp nullable), view_count (bigint default 0)",
            "paste_content": "Stored in S3 or blob storage, keyed by paste_id. Content is compressed (gzip) for pastes over 1KB. This separates metadata (fast queries) from content (bulk storage).",
            "users": "id (bigint PK), username (varchar unique), api_key (varchar unique), paste_count (int), storage_used_bytes (bigint), created_at (timestamp)"
        },
        "scaling_notes": "The architecture separates paste metadata from content. Metadata (ID, title, language, expiration) lives in a sharded relational database for fast lookups and filtering. The actual paste content is stored in object storage (S3), which handles the bulk storage efficiently and scales to petabytes. A Redis cache fronts both layers: hot paste metadata is cached with a TTL of 1 hour, and popular paste content is cached to avoid S3 reads for viral pastes. Paste IDs are generated using a pre-allocated ID range approach: each application server fetches a batch of IDs from a central counter (e.g., 1000 IDs at a time), encodes them in base62, eliminating per-paste coordination. The syntax highlighting is done client-side using a library like highlight.js, so the server only stores raw text. Expired pastes are cleaned up by a background worker that scans for pastes past their expiration time, deletes the S3 object, and removes the metadata row.",
        "failure_modes": [
            "S3 unavailability: cached pastes still serve but new pastes cannot be stored; queue creates and retry",
            "Redis cache failure: all reads go to S3 and the database; latency increases significantly but service continues",
            "Popular paste goes viral: single S3 key under extreme read pressure; CDN caching mitigates this for public pastes",
            "ID counter service failure: servers exhaust their pre-allocated batch; fall back to UUID-based IDs (longer URLs)"
        ],
        "trade_offs": [
            "Content in S3 vs database: S3 is cheaper for bulk storage and scales better but adds an extra hop for reads; database storage is simpler but expensive at scale",
            "Client-side vs server-side syntax highlighting: client-side reduces server load and supports more languages but increases page load time for large pastes",
            "Expiration by background job vs TTL: background jobs allow flexibility but introduce cleanup lag; TTL-based deletion (in Redis/DynamoDB) is automatic but limited to simple rules",
            "Public feed vs no feed: showing recent public pastes drives engagement but requires moderation to prevent spam and inappropriate content from appearing"
        ],
        "diagram_description": "Users create and view pastes through a load balancer and API Gateway. The Paste Service handles CRUD operations: on create, it generates a base62 ID from a pre-allocated counter, stores the content in S3 (gzip-compressed for large pastes), and writes metadata to a sharded PostgreSQL database. On read, the service first checks a Redis cache for both metadata and content. Cache misses for metadata fall through to PostgreSQL, and cache misses for content fall through to S3. Popular public pastes are also served through a CDN for additional caching. A background Expiration Worker periodically queries for expired pastes and removes both the S3 object and the database record. The Recent Pastes feed is powered by a Redis sorted set of the latest public paste IDs. Syntax highlighting is performed client-side using highlight.js with language auto-detection.",
        "order_index": 13
    },
    {
        "title": "Design Web Crawler",
        "slug": "design-web-crawler",
        "difficulty": "medium",
        "category": "data_intensive",
        "description": "Design a distributed web crawler that systematically discovers, fetches, and stores web pages for indexing. The system must handle politeness rules, deduplication, and scale to billions of pages while respecting robots.txt and site rate limits.",
        "requirements": {
            "functional": [
                "Crawl web pages starting from seed URLs and following discovered links",
                "Respect robots.txt rules and crawl-delay directives",
                "Detect and skip duplicate content (URL dedup and content dedup)",
                "Extract and normalize links from crawled pages",
                "Store crawled content for downstream indexing",
                "Support prioritized crawling (important pages first, fresh content preferred)"
            ],
            "non_functional": [
                "Crawl 10,000 pages per second (864 million pages/day)",
                "Scale horizontally by adding more crawler nodes",
                "No single domain receives more than 1 request per second (politeness)",
                "Recover from crawler node failures without losing progress",
                "Handle various content types and character encodings"
            ]
        },
        "estimation_hints": {
            "users": "N/A (infrastructure system). Target: crawl the top 50 billion web pages.",
            "storage": "Average page: 100KB HTML + 50KB metadata = 150KB. 864M pages/day * 150KB = 130TB/day. Index refresh cycle: 30 days.",
            "bandwidth": "10K pages/sec * 100KB = 1 Gbps outbound crawl traffic. Internal: ~5 Gbps for content storage.",
            "qps": "URL frontier dequeue: 10K/sec. robots.txt lookups: ~2K/sec (cached). Content hash dedup: 10K/sec."
        },
        "api_design": {
            "POST /api/v1/crawler/seeds": "Submit seed URLs to start or expand crawling. Input: list of URLs with priority.",
            "GET /api/v1/crawler/status": "Get crawler status: pages crawled, pages queued, active workers, error rate, pages/sec",
            "PUT /api/v1/crawler/config": "Update crawler configuration: max concurrent per domain, user agent, crawl depth limit, content type filters",
            "GET /api/v1/crawler/domain/:domain/stats": "Get per-domain crawl statistics: pages crawled, robots.txt rules, last crawl time, error count",
            "POST /api/v1/crawler/pause": "Pause/resume the crawler or specific domain crawls"
        },
        "schema_design": {
            "url_frontier": "url_hash (varchar PK - SHA256 prefix), url (text), domain (varchar), priority (float), depth (int), discovered_at (timestamp), state (enum: pending, in_progress, completed, failed), retry_count (int). Partitioned by domain for politeness grouping.",
            "crawled_pages": "url_hash (varchar PK), url (text), content_hash (varchar - for dedup), http_status (int), content_type (varchar), content_length (int), headers (jsonb), storage_key (varchar - S3 key for raw HTML), crawled_at (timestamp)",
            "robots_cache": "domain (varchar PK), rules (text - parsed robots.txt), fetched_at (timestamp), expires_at (timestamp). Cached per domain with 24-hour TTL.",
            "domain_state": "domain (varchar PK), last_request_at (timestamp), request_count (int), error_count (int), crawl_delay_seconds (int), avg_response_time_ms (int). Used for politeness scheduling."
        },
        "scaling_notes": "The URL frontier is the central data structure - a priority queue partitioned by domain. Each crawler worker pulls URLs from the frontier, respecting per-domain rate limits. The frontier is implemented as a two-level queue: a high-level priority queue of ready domains (domains whose rate limit cooldown has elapsed), and per-domain FIFO queues of URLs. Workers claim a domain from the priority queue, fetch one or more URLs from that domain's queue (respecting robots.txt and crawl-delay), and return the domain to the priority queue with an updated cooldown timestamp. This ensures global politeness. Content deduplication uses SimHash or MinHash on the page content to detect near-duplicate pages across different URLs. URL normalization (lowercase, remove fragments, sort query params) prevents crawling the same page via different URL variants. The frontier is distributed across multiple Redis instances or a custom distributed queue (like Apache Kafka with compaction). Crawled content is stored in S3 partitioned by crawl date for easy lifecycle management.",
        "failure_modes": [
            "Crawler node failure: URLs in in_progress state are timed out after 5 minutes and returned to the pending queue for retry",
            "Spider trap (infinite URL generation): detect by limiting crawl depth per domain and monitoring URL pattern repetition",
            "DNS resolution failure: cache DNS results aggressively; skip domains with persistent DNS failures",
            "Robot.txt fetch failure: if robots.txt cannot be fetched, conservatively delay crawling that domain for 24 hours",
            "Content dedup false positive: SimHash collision causes valid unique content to be skipped; tune similarity threshold carefully"
        ],
        "trade_offs": [
            "Breadth-first vs depth-first crawling: BFS discovers more sites quickly but may miss deep pages; priority-based BFS combines breadth with importance",
            "Politeness delay vs crawl speed: strict per-domain rate limiting (1 req/sec) slows crawl throughput but prevents being blocked; batch domain crawling helps",
            "Exact vs near-duplicate detection: exact URL dedup is cheap but misses content duplicates served from different URLs; near-duplicate detection catches more but costs O(N) comparisons",
            "Centralized vs decentralized frontier: a centralized frontier ensures global consistency but is a bottleneck; domain-based partitioning distributes the load at the cost of harder priority management"
        ],
        "diagram_description": "The system consists of a distributed URL Frontier, a fleet of Crawler Workers, and a Content Pipeline. Seed URLs enter the Frontier, which is partitioned by domain across multiple Redis or Kafka instances. A Scheduler assigns ready domains to available Crawler Workers based on rate-limit cooldowns. Each Worker fetches the robots.txt (from cache or fresh), then crawls pages from the assigned domain. Fetched pages go through a Content Pipeline: link extraction discovers new URLs that are normalized and deduplicated before being added back to the Frontier. The page content is hashed (SimHash) for near-duplicate detection, then stored in S3 for downstream indexing. A Domain State Tracker records per-domain statistics and adjusts crawl rates. A Monitoring Dashboard tracks crawl throughput, error rates, and frontier depth.",
        "order_index": 14
    },
    {
        "title": "Design Notification System",
        "slug": "design-notification-system",
        "difficulty": "medium",
        "category": "infrastructure",
        "description": "Design a scalable notification system that delivers messages across multiple channels (push, email, SMS, in-app) with user preferences, template management, rate limiting, and delivery tracking. The system must handle millions of notifications per hour reliably.",
        "requirements": {
            "functional": [
                "Send notifications via push (iOS/Android), email, SMS, and in-app channels",
                "Users can configure notification preferences per channel and notification type",
                "Template management for notification content with variable substitution",
                "Priority levels (critical, high, normal, low) with different delivery guarantees",
                "Delivery tracking and retry for failed deliveries",
                "Batching and digest support (aggregate multiple notifications into one)"
            ],
            "non_functional": [
                "Critical notifications delivered within 30 seconds",
                "Process 10 million notifications per hour",
                "At-least-once delivery guarantee",
                "99.9% delivery success rate (excluding user-side issues like invalid tokens)",
                "Horizontal scaling by adding worker nodes"
            ]
        },
        "estimation_hints": {
            "users": "100M registered users. 10M notifications/hour = ~2,800/sec average, 10K/sec peak.",
            "storage": "Notification records: ~500 bytes each. 10M/hour * 24 * 365 = 87B/year * 500 bytes = 43TB/year. Templates: negligible.",
            "bandwidth": "Outbound to providers (APNS, FCM, email SMTP, SMS API): ~50 Mbps. Inbound triggers: ~10 Mbps.",
            "qps": "Trigger ingestion: 2,800/sec avg. Provider API calls: ~3,500/sec (some notifications go to multiple channels). Preference lookups: ~2,800/sec."
        },
        "api_design": {
            "POST /api/v1/notifications/send": "Trigger a notification. Input: user_ids (list), template_id, variables (dict), channels (optional override), priority",
            "GET /api/v1/notifications/:notificationId/status": "Get delivery status for a notification across all channels",
            "PUT /api/v1/users/:userId/preferences": "Update notification preferences: per notification_type and channel, enabled/disabled, quiet hours",
            "GET /api/v1/users/:userId/inbox?cursor=&limit=": "Get in-app notification inbox with read/unread status and pagination",
            "POST /api/v1/templates": "Create or update a notification template with subject, body (with {{variable}} placeholders), and per-channel variants"
        },
        "schema_design": {
            "notifications": "id (uuid PK), user_id (bigint FK), template_id (varchar FK), variables (jsonb), priority (enum), status (enum: pending, processing, delivered, partially_delivered, failed), channels_status (jsonb - per-channel delivery status), created_at (timestamp), delivered_at (timestamp nullable). Partitioned by month.",
            "notification_preferences": "user_id (bigint), notification_type (varchar), channel (varchar), enabled (boolean), quiet_hours_start (time nullable), quiet_hours_end (time nullable). PK (user_id, notification_type, channel).",
            "templates": "id (varchar PK), name (varchar), notification_type (varchar), subject_template (text), body_template (text), channel_variants (jsonb - per-channel body overrides), version (int), updated_at (timestamp)",
            "device_tokens": "user_id (bigint), platform (enum: ios, android, web), token (varchar), app_version (varchar), updated_at (timestamp). PK (user_id, platform, token). Tokens can become stale."
        },
        "scaling_notes": "The notification pipeline uses Kafka as the central message bus. When a notification is triggered, the API server publishes an event to a Kafka topic partitioned by priority. High-priority consumers process the critical/high topics with more workers and lower batching. The processing pipeline has three stages: (1) Preference Check - filters out notifications the user has opted out of or that fall in quiet hours, (2) Template Rendering - resolves the template with variables for each active channel, (3) Channel Delivery - sends to the appropriate provider (APNS for iOS push, FCM for Android, SendGrid/SES for email, Twilio for SMS). Each provider integration runs as a separate consumer group for independent scaling. Failed deliveries go to a retry topic with exponential backoff. For batch/digest notifications, a time-window aggregator collects events for the same user+type and produces a single digest after the window closes. Device token cleanup runs periodically, removing tokens that APNS/FCM report as invalid.",
        "failure_modes": [
            "APNS/FCM provider outage: push notifications queue in Kafka retry topic; delivered when provider recovers; in-app notification serves as fallback",
            "Email provider rate limit exceeded: back off and retry; spread load across multiple email providers (SES + SendGrid)",
            "Stale device token: push delivery fails silently; APNS feedback service reports invalid tokens for cleanup",
            "Kafka consumer lag: notifications are delayed; auto-scale consumer groups based on lag metrics",
            "Template rendering error: invalid variable in template causes failure for all recipients; validate templates on publish"
        ],
        "trade_offs": [
            "At-least-once vs exactly-once delivery: at-least-once is simpler and more reliable but may result in duplicate notifications; clients should be idempotent",
            "Per-notification processing vs batching: per-notification provides fastest delivery but wastes provider API calls; batching reduces costs but adds latency for non-critical notifications",
            "Centralized vs per-channel queues: centralized queue simplifies management but a slow channel (SMS) can back up others; per-channel queues isolate failures",
            "Push notification payload size: rich notifications with images and actions engage better but APNS limits payload to 4KB; use mutable-content to fetch additional data client-side"
        ],
        "diagram_description": "Event sources (API calls, cron jobs, service events) publish notification triggers to a Kafka topic partitioned by priority. A Preference Filter consumer checks user preferences and quiet hours, dropping opted-out notifications. Approved notifications flow to the Template Renderer, which resolves templates with variables and produces per-channel messages. Channel-specific Kafka topics feed dedicated Delivery Workers: a Push Worker sends to APNS/FCM, an Email Worker sends via SES/SendGrid, an SMS Worker sends via Twilio, and an In-App Worker writes to the user's notification inbox (DynamoDB). Each delivery worker reports success or failure back to a Status Tracker that updates the notification record. Failed deliveries go to a Retry Topic with exponential backoff. A Digest Aggregator collects low-priority notifications into batched digests on a configurable time window.",
        "order_index": 15
    },
    {
        "title": "Design Payment System",
        "slug": "design-payment-system",
        "difficulty": "hard",
        "category": "infrastructure",
        "description": "Design a payment processing system that handles credit card transactions, wallet balances, refunds, and settlement. The system must guarantee exactly-once payment execution, maintain strict financial consistency, and comply with PCI-DSS requirements.",
        "requirements": {
            "functional": [
                "Process credit/debit card payments through payment gateways (Stripe, Adyen)",
                "Maintain wallet balances with top-up and withdrawal",
                "Handle refunds (full and partial) back to original payment method",
                "Support multiple currencies with exchange rate management",
                "Generate transaction ledger entries for every financial event",
                "Settlement: batch transfer funds to merchants on a schedule"
            ],
            "non_functional": [
                "Exactly-once payment execution (no double charges, no lost payments)",
                "Process 10,000 transactions per second at peak",
                "Transaction processing latency under 2 seconds",
                "PCI-DSS Level 1 compliance for card data handling",
                "99.999% availability for the payment processing path"
            ]
        },
        "estimation_hints": {
            "users": "50M active users, 10K transactions/sec peak, 500M transactions/day",
            "storage": "Each transaction: ~2KB. 500M/day * 365 * 7 years (retention) = 1.2T records * 2KB = 2.5PB",
            "bandwidth": "Gateway API calls: 10K/sec * 1KB = 10MB/sec. Ledger writes: 10K/sec * 500 bytes = 5MB/sec.",
            "qps": "Payment processing: 10K/sec peak. Balance reads: 50K/sec. Ledger queries: 5K/sec."
        },
        "api_design": {
            "POST /api/v1/payments": "Initiate a payment. Input: amount, currency, payment_method_id, idempotency_key, metadata. Returns: payment_id, status (pending/succeeded/failed)",
            "POST /api/v1/payments/:paymentId/refund": "Refund a payment (full or partial). Input: amount (optional for partial), reason. Idempotent by payment_id + amount.",
            "GET /api/v1/wallets/:userId/balance": "Get wallet balance in all currencies",
            "POST /api/v1/wallets/:userId/topup": "Add funds to wallet. Input: amount, currency, payment_method_id, idempotency_key",
            "GET /api/v1/ledger/:accountId?start_date=&end_date=&cursor=": "Query double-entry ledger for an account with date range and pagination"
        },
        "schema_design": {
            "payments": "id (uuid PK), idempotency_key (varchar unique), user_id (bigint FK), amount_cents (bigint), currency (varchar 3), status (enum: pending, processing, succeeded, failed, refunded), payment_method_id (uuid FK), gateway (varchar), gateway_reference (varchar), error_code (varchar nullable), created_at (timestamp), updated_at (timestamp). Idempotency key ensures exactly-once processing.",
            "ledger_entries": "id (bigint PK), payment_id (uuid FK), debit_account (varchar), credit_account (varchar), amount_cents (bigint), currency (varchar 3), entry_type (enum: payment, refund, settlement, fee), created_at (timestamp). Immutable, append-only. Every financial event creates balanced debit/credit entries.",
            "wallets": "user_id (bigint), currency (varchar 3), balance_cents (bigint), version (bigint - for optimistic locking). PK (user_id, currency). Balance changes use SELECT FOR UPDATE.",
            "settlement_batches": "id (uuid PK), merchant_id (bigint FK), total_amount_cents (bigint), currency (varchar 3), transaction_count (int), status (enum: pending, processing, settled, failed), settlement_date (date), created_at (timestamp)"
        },
        "scaling_notes": "Financial consistency is the paramount concern. Every payment uses an idempotency key: the first request creates the payment, and duplicate requests with the same key return the existing result without reprocessing. The payment state machine transitions through well-defined states (pending, processing, succeeded, failed) using optimistic locking. The double-entry ledger ensures every credit has a matching debit - the sum of all entries for any financial event must be zero. Wallet balance updates use SELECT FOR UPDATE within a serializable transaction to prevent race conditions. For scalability, payments are sharded by user_id, ensuring all of a user's transactions land on the same shard for strong consistency. The gateway integration layer uses a circuit breaker pattern: if Stripe fails, traffic routes to Adyen. Settlement runs as a nightly batch job that aggregates completed transactions per merchant and initiates bank transfers. PCI-DSS compliance requires that raw card data never touches application servers - tokenized via the gateway's client-side SDK.",
        "failure_modes": [
            "Payment gateway timeout: payment status is unknown; query the gateway for the transaction status before retrying to prevent double charge",
            "Database failure during payment: the idempotency key ensures the payment is either committed or can be safely retried",
            "Wallet balance goes negative due to race condition: serializable isolation on wallet updates prevents this; if somehow negative, block further debits",
            "Settlement batch failure: mark batch as failed, investigate, and re-run; merchant funds are held safely in the platform's settlement account",
            "Currency exchange rate stale: use a cached rate with a staleness threshold; reject transactions if the rate is too old"
        ],
        "trade_offs": [
            "Synchronous vs async payment processing: synchronous gives immediate feedback to the user but ties up server resources; async with webhooks scales better but complicates the UX",
            "Double-entry ledger vs simple transaction log: double-entry is more complex but provides built-in auditability and catches accounting errors; essential for financial systems",
            "Optimistic vs pessimistic locking for wallets: pessimistic (SELECT FOR UPDATE) prevents all race conditions but reduces concurrency; optimistic locking with retries handles most cases with less contention",
            "Multi-gateway vs single gateway: multiple gateways provide redundancy and routing optimization but double the integration and testing surface"
        ],
        "diagram_description": "Payment requests arrive at the API Gateway, which routes to the Payment Service. The Payment Service first checks the idempotency key in a dedicated Idempotency Store (Redis or DynamoDB). New payments are recorded with status 'pending' in the sharded Payments Database (PostgreSQL). The Payment Service calls the Payment Gateway Adapter, which routes to the optimal gateway (Stripe or Adyen) via a circuit breaker. On success, the service updates the payment status, writes double-entry Ledger Entries, and publishes a payment.succeeded event to Kafka. The Wallet Service subscribes to payment events and updates wallet balances using serializable transactions. A Settlement Service runs nightly, aggregating completed transactions per merchant and initiating bank transfers. All card data is tokenized client-side by the gateway SDK - application servers only handle tokens. An Audit Service subscribes to all financial events for compliance reporting.",
        "order_index": 16
    },
    {
        "title": "Design Chat System",
        "slug": "design-chat-system",
        "difficulty": "medium",
        "category": "real_time",
        "description": "Design a real-time chat system supporting one-on-one conversations, group chats, message history, and online presence. Unlike WhatsApp (which emphasizes encryption and mobile), this focuses on a web-first platform with rich features like message editing, reactions, and typing indicators.",
        "requirements": {
            "functional": [
                "Real-time one-on-one and group messaging",
                "Message editing and deletion with edit history",
                "Typing indicators showing who is currently typing",
                "Emoji reactions on messages",
                "Message read receipts per user in group chats",
                "File and image attachments with inline preview"
            ],
            "non_functional": [
                "Message delivery under 100ms for online users",
                "Support 5 million concurrent WebSocket connections",
                "Persistent message history with fast scroll-back",
                "99.9% uptime",
                "Support groups with up to 500 members"
            ]
        },
        "estimation_hints": {
            "users": "20M registered users, 5M DAU, 5M concurrent connections at peak",
            "storage": "200M messages/day * 200 bytes avg = 40GB/day. File attachments: ~2TB/day. Total: ~30TB/year messages.",
            "bandwidth": "WebSocket messages: ~100MB/sec. File serving: ~2 Gbps. Typing indicators: ~50MB/sec (short-lived).",
            "qps": "Message sends: ~2,300/sec. Typing indicator broadcasts: ~10K/sec. Presence updates: ~5K/sec. History reads: ~5K/sec."
        },
        "api_design": {
            "WS /api/v1/ws/connect": "Establish WebSocket connection. Receives real-time messages, typing indicators, presence updates, and reactions.",
            "POST /api/v1/messages": "Send a message to a conversation. Input: conversation_id, content, attachments. Returns: message with server-assigned ID and timestamp.",
            "PUT /api/v1/messages/:messageId": "Edit a message. Stores edit history. Broadcasts update to conversation members.",
            "GET /api/v1/conversations/:conversationId/messages?before=&limit=": "Fetch message history with cursor-based backward pagination for scroll-back",
            "POST /api/v1/messages/:messageId/reactions": "Add or remove a reaction (emoji) on a message",
            "POST /api/v1/conversations/:conversationId/typing": "Signal that the user is typing (broadcast to other members, auto-expires after 3 seconds)"
        },
        "schema_design": {
            "messages": "id (bigint PK, snowflake), conversation_id (bigint FK), sender_id (bigint FK), content (text), attachments (jsonb), edited (boolean), edit_history (jsonb nullable), deleted (boolean), created_at (timestamp), edited_at (timestamp nullable). Partitioned by conversation_id.",
            "conversations": "id (bigint PK), type (enum: direct, group), name (varchar nullable), creator_id (bigint FK), member_count (int), last_message_at (timestamp), created_at (timestamp)",
            "conversation_members": "conversation_id (bigint), user_id (bigint), role (enum: owner, admin, member), last_read_message_id (bigint), muted (boolean), joined_at (timestamp). PK (conversation_id, user_id).",
            "reactions": "message_id (bigint), user_id (bigint), emoji (varchar 50), created_at (timestamp). PK (message_id, user_id, emoji).",
            "read_receipts": "conversation_id (bigint), user_id (bigint), last_read_message_id (bigint), read_at (timestamp). PK (conversation_id, user_id). Used for per-user read indicators in group chats."
        },
        "scaling_notes": "The WebSocket layer is the primary scaling challenge. Gateway servers each handle ~50K connections (limited by file descriptors and memory). A connection registry in Redis maps each user to their gateway server for message routing. When user A sends a message in a conversation, the Chat Service writes it to the database and publishes to a Redis Pub/Sub channel keyed by conversation_id. Each gateway server subscribes to the channels of its connected users' conversations. For group messages, the publish fans out to all subscribed gateways. Typing indicators use a lightweight UDP-based broadcast that skips persistence entirely - they are ephemeral by nature. Message history uses PostgreSQL with composite indexes on (conversation_id, created_at) for fast scroll-back queries. Read receipts are updated in batches (every 5 seconds) to reduce write frequency. Attachment files are uploaded to S3 with pre-signed URLs and thumbnails generated asynchronously.",
        "failure_modes": [
            "Gateway server crash: connected users reconnect to another gateway; missed messages are fetched via history API using last_read cursor",
            "Redis Pub/Sub message loss: Redis Pub/Sub does not persist messages; clients poll for gaps using the history API on reconnect",
            "Database write failure: message send fails; client retries with the same idempotency key",
            "Typing indicator flood: a misbehaving client sends excessive typing events; rate-limit at the gateway (max 1 per 2 seconds per user per conversation)",
            "Large group message fan-out: a 500-member group generates 500 WebSocket pushes; batch delivery across gateways"
        ],
        "trade_offs": [
            "Redis Pub/Sub vs Kafka for real-time delivery: Redis Pub/Sub is lower latency but fire-and-forget (no persistence); Kafka guarantees delivery but adds latency. Pub/Sub for online delivery, history API for catch-up.",
            "Server-assigned vs client-assigned message IDs: server-assigned IDs guarantee uniqueness but require a round trip; client-generated UUIDs enable optimistic UI but risk collisions",
            "Persisting typing indicators vs ephemeral: not persisting saves storage and write load but means typing state is lost on gateway failover; acceptable trade-off for a transient signal",
            "Per-message read receipts vs conversation-level: per-message receipts show exactly which messages each user has read but generate more writes; conversation-level (watermark) is cheaper but less precise"
        ],
        "diagram_description": "Clients connect via WebSocket to a pool of Gateway Servers behind a load balancer with sticky sessions. The Gateway Servers maintain a mapping of connected users in a shared Redis Connection Registry. When a message is sent, the Chat Service writes it to sharded PostgreSQL and publishes it to a Redis Pub/Sub channel for the conversation. Subscribed Gateway Servers push the message to their connected members. For offline users, the message is stored in the database and delivered on their next connection. Typing indicators flow directly through Redis Pub/Sub without persistence. File attachments are uploaded via pre-signed S3 URLs, with a Thumbnail Service generating previews asynchronously. Read receipts are batched and written every 5 seconds. A Presence Service uses Redis with heartbeat TTLs to track online/offline status. The Notification Service pushes mobile notifications for offline users via APNS/FCM.",
        "order_index": 17
    },
    {
        "title": "Design News Feed",
        "slug": "design-news-feed",
        "difficulty": "medium",
        "category": "web_scale",
        "description": "Design a social media news feed system that aggregates posts from friends and followed accounts into a personalized, ranked timeline. The system must handle the fan-out problem at scale and balance chronological ordering with relevance-based ranking.",
        "requirements": {
            "functional": [
                "Display a personalized feed of posts from followed users/friends",
                "Rank posts by relevance (engagement signals, recency, user interests)",
                "Support multiple content types (text, image, video, link shares)",
                "Infinite scroll with cursor-based pagination",
                "Feed refreshes show new content at the top with a 'new posts' indicator",
                "Content filtering (hide, report, not interested)"
            ],
            "non_functional": [
                "Feed load time under 300ms",
                "Support 500 million daily active users",
                "Fresh content appears within 30 seconds of posting",
                "Ranking model re-ranks top candidates in under 50ms",
                "Handle users who follow up to 5,000 accounts"
            ]
        },
        "estimation_hints": {
            "users": "500M DAU, average user follows 300 accounts, 100M new posts/day",
            "storage": "Pre-computed feed cache: ~2KB/user * 500M = 1TB in Redis. Post metadata: ~50TB",
            "bandwidth": "Feed reads: ~1M/sec at peak. Each feed response: ~50KB (20 posts with metadata). Total: ~50 GB/sec.",
            "qps": "Feed reads: 1M/sec peak. Post publishes: ~1,200/sec. Engagement events (like, comment): ~500K/sec."
        },
        "api_design": {
            "GET /api/v1/feed?cursor=&limit=20": "Fetch ranked feed for authenticated user. Returns posts with engagement counts, author info, and next cursor.",
            "GET /api/v1/feed/updates?since_cursor=": "Check for new posts since the last loaded cursor; returns count for 'N new posts' indicator",
            "POST /api/v1/feed/actions/hide": "Hide a post from the feed; used as negative signal for ranking",
            "POST /api/v1/feed/actions/not-interested": "Mark a topic or author as not interesting; adjusts future ranking",
            "GET /api/v1/feed/trending": "Get trending/viral posts outside the user's network for discovery"
        },
        "schema_design": {
            "posts": "id (bigint PK), author_id (bigint FK), content_type (enum: text, image, video, link), text (text), media_urls (jsonb), link_url (varchar nullable), like_count (bigint), comment_count (int), share_count (int), created_at (timestamp)",
            "feed_cache": "user_id (bigint) -> sorted set of (post_id, score). Redis sorted set. Score combines relevance rank and recency. Stores top 500 post IDs per user.",
            "feed_interactions": "user_id (bigint), post_id (bigint), interaction_type (enum: view, like, comment, share, hide, not_interested), timestamp (timestamp). Used to train the ranking model and filter already-seen content.",
            "user_interests": "user_id (bigint PK), topic_scores (jsonb - topic to affinity score mapping), updated_at (timestamp). Updated by a batch pipeline from interaction history."
        },
        "scaling_notes": "The news feed uses a hybrid fan-out strategy similar to Twitter's approach. When a user with fewer than 10K followers publishes a post, the Fan-out Service pushes the post ID into each follower's pre-computed feed cache in Redis. For users with more than 10K followers, posts are fetched and merged at read time to avoid write amplification. At read time, the Feed Service retrieves the user's cached feed, supplements it with on-demand posts from high-follower accounts, and passes the top ~200 candidates through a lightweight ML ranking model. The ranking model scores each post based on: predicted engagement probability, content type preference, author affinity, recency, and diversity (to avoid showing too many posts from one author or topic). The ranked feed is paginated and returned. Engagement events (likes, comments) update counters asynchronously via Kafka. The interest model is updated hourly by a batch pipeline processing interaction logs.",
        "failure_modes": [
            "Feed cache miss (Redis): fall back to an on-demand feed generation query against the posts table; 2-5x slower but functional",
            "Ranking model service timeout: return chronologically ordered feed without ML ranking; slightly lower engagement but fast",
            "Fan-out service lag: new posts from normal users appear delayed in followers' feeds; tolerable up to 60 seconds",
            "Engagement counter drift: like/comment counts in the feed may lag by a few seconds behind real-time",
            "Cold start for new users: no interaction history means the ranking model cannot personalize; use popularity-based feed with editorial picks"
        ],
        "trade_offs": [
            "Relevance ranking vs chronological: ranked feeds increase engagement metrics but users complain about missing timely posts; offer a toggle or use time-decay in the ranking function",
            "Fan-out on write cost: pushing to 300 followers per post costs ~300 Redis writes per post but makes reads instant; without it, each feed read would require querying 300 authors",
            "Feed cache size per user: storing 500 post IDs (4KB) per 500M users requires 2TB of Redis; reducing to 200 saves memory but increases cache miss rate for heavy scrollers",
            "Real-time ranking vs pre-ranked: real-time scoring of 200 candidates in 50ms requires GPU inference servers; pre-ranking in batch is cheaper but shows staler rankings"
        ],
        "diagram_description": "When a user publishes a post, the Post Service writes it to the posts database and publishes an event to Kafka. The Fan-out Service consumes post events, looks up the author's followers from the Social Graph Service, and for accounts with under 10K followers pushes the post ID into each follower's Redis feed cache (sorted by a preliminary score). When a user requests their feed, the Feed Service reads their cached post IDs, supplements with on-demand posts from high-follower accounts, fetches full post metadata from the Post Cache (Redis/Memcached backed by the posts database), and passes the candidate set to the Ranking Service. The Ranking Service runs an ML model that scores each post based on engagement prediction, user interests, recency, and diversity. The ranked results are returned with pagination. An Engagement Pipeline processes likes, comments, and view events via Kafka, updating counters and feeding the recommendation model training pipeline.",
        "order_index": 18
    },
    {
        "title": "Design Ticket Booking",
        "slug": "design-ticket-booking",
        "difficulty": "medium",
        "category": "real_time",
        "description": "Design an online ticket booking system (like BookMyShow or Ticketmaster) for events, movies, and concerts. The system must handle seat selection with real-time availability, temporary holds during checkout, and prevent double-booking under high concurrency.",
        "requirements": {
            "functional": [
                "Browse events with filtering by date, location, category, and price range",
                "View venue seating map with real-time seat availability",
                "Select seats and hold them temporarily during checkout (5-minute reservation)",
                "Complete booking with payment processing",
                "Generate e-tickets with QR codes after successful booking",
                "Support waitlists for sold-out events"
            ],
            "non_functional": [
                "Seat selection and hold must complete within 2 seconds",
                "Zero double-bookings (strong consistency for seat allocation)",
                "Handle 100K concurrent users during popular event on-sales",
                "Temporary holds auto-expire after 5 minutes if checkout is not completed",
                "99.9% availability during on-sale windows"
            ]
        },
        "estimation_hints": {
            "users": "50M registered users. 1M tickets sold/day across all events. Peak: 500K concurrent during a popular on-sale.",
            "storage": "Events: ~500K active. Seats: ~50M active seat records. Bookings: ~1M/day * 1KB = 1GB/day. Total: ~5TB",
            "bandwidth": "Seat map loads: ~50K/sec during peak. Each seat map: ~20KB. Total: ~1 Gbps peak.",
            "qps": "Seat availability: 50K/sec. Hold seat: 10K/sec. Confirm booking: 5K/sec. Event search: 20K/sec."
        },
        "api_design": {
            "GET /api/v1/events/search?q=&city=&date=&category=&cursor=": "Search and filter events with pagination",
            "GET /api/v1/events/:eventId/seats?section=": "Get real-time seat availability map for an event section. Returns seat grid with status (available/held/booked).",
            "POST /api/v1/bookings/hold": "Temporarily hold selected seats for 5 minutes. Input: event_id, seat_ids. Returns: hold_id, expires_at. Fails if any seat is not available.",
            "POST /api/v1/bookings/confirm": "Confirm booking and process payment. Input: hold_id, payment_method_id. Returns: booking with e-ticket details.",
            "GET /api/v1/bookings/:bookingId": "Get booking details with e-ticket QR code data",
            "POST /api/v1/events/:eventId/waitlist": "Join waitlist for a sold-out event"
        },
        "schema_design": {
            "events": "id (bigint PK), title (varchar), description (text), venue_id (bigint FK), category (varchar), start_time (timestamp), end_time (timestamp), total_seats (int), available_seats (int), status (enum: upcoming, on_sale, sold_out, completed), on_sale_at (timestamp)",
            "seats": "id (bigint PK), event_id (bigint FK), section (varchar), row (varchar), number (int), price_cents (int), status (enum: available, held, booked), hold_expires_at (timestamp nullable), held_by_user (bigint nullable), version (bigint - optimistic lock). Unique (event_id, section, row, number).",
            "bookings": "id (bigint PK), user_id (bigint FK), event_id (bigint FK), seat_ids (bigint array), total_price_cents (int), status (enum: held, confirmed, cancelled, refunded), payment_id (uuid nullable), created_at (timestamp), confirmed_at (timestamp nullable)",
            "waitlist": "event_id (bigint), user_id (bigint), position (int), seat_count (int), joined_at (timestamp). PK (event_id, user_id). FIFO queue per event."
        },
        "scaling_notes": "The critical challenge is seat allocation under extreme concurrency during popular on-sales. Each seat has an optimistic lock (version column): the hold operation does a conditional UPDATE that sets status='held' only WHERE status='available' AND version=expected_version. If the update affects 0 rows, the seat was taken by another user. For a multi-seat booking, all seats must be held atomically within a single transaction to prevent partial holds. The 5-minute hold expiration is enforced two ways: (1) a background job that scans for expired holds every 30 seconds, and (2) a lazy check where reads treat holds past their expiration as available. To handle the thundering herd of a popular on-sale, a virtual waiting room is implemented: when traffic exceeds a threshold, users are placed in a queue and admitted in batches. This converts an uncontrolled stampede into a controlled flow. Seat availability maps are cached in Redis with fine-grained invalidation on status changes. Event search uses Elasticsearch.",
        "failure_modes": [
            "Payment failure after seat hold: seats remain held until the 5-minute TTL expires, then automatically release for others to book",
            "Hold expiration job failure: lazy expiration on read ensures seats are still released, but the background job handles cases where no one reads the seat",
            "Database connection exhaustion during on-sale spike: the virtual waiting room caps concurrent booking attempts; connection pooling with pgbouncer helps",
            "Double-hold race condition: optimistic locking on the seat version column prevents this; at most one user holds any given seat",
            "QR code generation service failure: booking succeeds but ticket delivery is delayed; retry ticket generation asynchronously"
        ],
        "trade_offs": [
            "Optimistic vs pessimistic locking for seats: optimistic locking (version check) allows higher concurrency but requires retry logic when conflicts occur; pessimistic (SELECT FOR UPDATE) guarantees success but serializes all attempts for the same seat",
            "Virtual waiting room vs first-come-first-served: waiting room adds perceived unfairness (random queue position) but prevents system overload and provides a better experience than error pages",
            "Real-time seat map vs cached: real-time is more accurate but requires a database query per seat section view; caching with 1-second invalidation provides near-real-time at 100x less load",
            "Hold timeout duration: longer holds (10 min) give users more time to pay but lock inventory; shorter holds (3 min) release faster but may frustrate slow payers"
        ],
        "diagram_description": "Users access the system through a CDN and load balancer. During high-demand on-sales, a Virtual Waiting Room queues users and admits them in controlled batches. The Event Service serves event listings from Elasticsearch. The Seat Service manages seat availability in a PostgreSQL cluster with optimistic locking, fronted by a Redis cache for the seat map. The Booking Service orchestrates the hold-confirm flow: it atomically holds selected seats in a transaction, starts a 5-minute timer, and on confirmation calls the Payment Service. Successful bookings trigger the Ticket Service to generate e-tickets with QR codes. A Hold Expiration Worker runs every 30 seconds to release expired holds. The Waitlist Service manages per-event FIFO queues and notifies users when seats become available. All booking events flow through Kafka for analytics and fraud detection.",
        "order_index": 19
    },
    {
        "title": "Design File Storage",
        "slug": "design-file-storage",
        "difficulty": "medium",
        "category": "data_intensive",
        "description": "Design a cloud file storage and synchronization service like Dropbox or Google Drive. The system must support file upload/download, folder hierarchy, real-time sync across devices, file versioning, and collaborative sharing.",
        "requirements": {
            "functional": [
                "Upload, download, and delete files and folders",
                "Real-time file synchronization across multiple devices",
                "File versioning with the ability to restore previous versions",
                "Share files and folders with other users (view/edit permissions)",
                "Support for large files (up to 50GB) with resumable uploads",
                "Conflict resolution when multiple devices modify the same file"
            ],
            "non_functional": [
                "File sync latency under 10 seconds for small files",
                "Support 500 million users and 1 billion files",
                "99.99% durability (no data loss)",
                "Support 10 million concurrent sync clients",
                "Bandwidth-efficient sync (only transfer changed file blocks)"
            ]
        },
        "estimation_hints": {
            "users": "500M users, 1B files, 100M DAU with sync clients running",
            "storage": "Average file: 1MB. 1B files * 1MB = 1EB. With versioning (avg 3 versions): 3EB. Block-level dedup reduces to ~1EB.",
            "bandwidth": "File uploads: ~100 Gbps. Downloads: ~200 Gbps. Sync metadata: ~10 Gbps.",
            "qps": "Metadata operations (list, stat): 500K/sec. File uploads: 50K/sec. Sync notifications: 1M/sec."
        },
        "api_design": {
            "POST /api/v1/files/upload/chunked/init": "Initialize a chunked upload. Input: filename, size, parent_folder_id. Returns: upload_id, chunk_size, upload_url",
            "PUT /api/v1/files/upload/chunked/:uploadId/:chunkIndex": "Upload a single chunk. Client computes block hashes; server skips blocks already stored (dedup).",
            "GET /api/v1/files/:fileId/download": "Download a file. Supports range requests for resumable downloads.",
            "GET /api/v1/files/:fileId/versions": "List version history for a file",
            "POST /api/v1/files/:fileId/share": "Share a file or folder. Input: user_email, permission (view/edit). Returns: share_link",
            "GET /api/v1/sync/changes?cursor=": "Long-poll endpoint: returns list of changes since cursor, or blocks until changes occur (timeout 90 seconds)"
        },
        "schema_design": {
            "file_metadata": "id (bigint PK), name (varchar), parent_folder_id (bigint FK nullable), owner_id (bigint FK), size_bytes (bigint), content_hash (varchar), mime_type (varchar), version (int), is_folder (boolean), is_deleted (boolean), created_at (timestamp), modified_at (timestamp). Tree structure via parent_folder_id.",
            "file_versions": "file_id (bigint FK), version (int), content_hash (varchar), size_bytes (bigint), modified_by (bigint FK), modified_at (timestamp), block_list (jsonb - ordered list of block hashes). PK (file_id, version).",
            "blocks": "hash (varchar PK - SHA256 of block content), size_bytes (int), storage_path (varchar), reference_count (int). Content-addressable store. Blocks are shared across files via dedup.",
            "sync_journal": "id (bigint PK, auto-increment), user_id (bigint), file_id (bigint), change_type (enum: create, update, delete, move, share), timestamp (timestamp). Append-only log. Cursor for sync is the last processed journal ID.",
            "shares": "file_id (bigint), shared_with_user_id (bigint), permission (enum: view, edit), shared_by (bigint FK), created_at (timestamp). PK (file_id, shared_with_user_id)."
        },
        "scaling_notes": "The key optimization is block-level deduplication and delta sync. Files are split into fixed-size blocks (typically 4MB), each identified by its SHA-256 hash. When uploading, the client computes block hashes and sends them to the server. The server responds with which blocks it already has (from this or any other user's files), and the client only uploads missing blocks. This dramatically reduces upload bandwidth for modified files (only changed blocks are transferred) and storage for duplicate content across users. The sync protocol uses a journal-based approach: every file operation appends to a per-user sync journal. Sync clients long-poll the changes endpoint, receiving a stream of changes since their last cursor. On conflict (two devices modify the same file), the server keeps both versions and marks one as a conflict copy. Metadata is stored in sharded MySQL, file blocks in S3 with a separate block index. Notification of changes uses a WebSocket push channel for online clients, falling back to long-polling.",
        "failure_modes": [
            "Block storage (S3) failure: uploads fail; retry from the last successful chunk. Downloads for cached/replicated blocks may still work.",
            "Sync journal lag: clients receive delayed change notifications; eventual consistency is acceptable for sync (seconds, not minutes)",
            "Conflict during simultaneous edit: both versions are saved; one is marked as a conflict copy for the user to resolve manually",
            "Dedup hash collision (SHA-256): astronomically unlikely (2^-128 probability) but would cause data corruption; use a secondary hash for critical files",
            "Large folder listing: a folder with 100K files takes significant time to list; implement pagination and lazy loading in the client"
        ],
        "trade_offs": [
            "Block-level vs file-level dedup: block-level dedup catches partial changes and cross-file duplicates but adds complexity in block management and reference counting; file-level is simpler but wastes storage on small edits",
            "Fixed vs variable-size blocks: fixed blocks are simpler to manage but miss optimization opportunities; variable blocks (Rabin fingerprint) align boundaries to content, improving dedup ratio by ~20% but adding computational overhead",
            "Immediate sync vs batched: immediate sync provides real-time collaboration but generates more traffic; batching changes over a few seconds reduces network load at the cost of slightly delayed sync",
            "Conflict copies vs operational transform: conflict copies are simple but require manual resolution; operational transform (like Google Docs) enables real-time co-editing but is extremely complex to implement for arbitrary file types"
        ],
        "diagram_description": "Sync clients run on user devices, monitoring local file changes. When a change is detected, the client splits the file into blocks, computes SHA-256 hashes, and sends the hash list to the Block Server. The Block Server checks which blocks are already stored in the Block Index (a hash-to-storage-path mapping in Redis/DynamoDB) and requests only missing blocks from the client. New blocks are written to S3 Block Storage. The Metadata Service updates the file's metadata and block list in sharded MySQL and appends to the Sync Journal. Other devices long-poll the Sync Service's changes endpoint, receive the updated block list, download only the new/changed blocks, and reconstruct the file locally. A Notification Service pushes change events via WebSocket for faster sync. The Sharing Service manages permissions and generates share links. A Garbage Collector periodically removes unreferenced blocks (reference_count = 0) from S3.",
        "order_index": 20
    },
    {
        "title": "Design Monitoring System",
        "slug": "design-monitoring-system",
        "difficulty": "medium",
        "category": "infrastructure",
        "description": "Design a distributed monitoring and alerting system that collects metrics, logs, and traces from thousands of services. The system must support real-time dashboards, configurable alerts, and efficient long-term storage for observability data.",
        "requirements": {
            "functional": [
                "Collect metrics (counters, gauges, histograms) from application and infrastructure sources",
                "Ingest structured logs from thousands of services",
                "Distributed tracing with trace and span correlation",
                "Configurable alerting rules with escalation policies",
                "Real-time dashboards with custom queries and visualizations",
                "Anomaly detection on metric time series"
            ],
            "non_functional": [
                "Ingest 10 million metrics data points per second",
                "Ingest 1 million log lines per second",
                "Query latency under 2 seconds for dashboards covering 24-hour windows",
                "Alert evaluation latency under 30 seconds",
                "Retain detailed data for 30 days, aggregated data for 1 year"
            ]
        },
        "estimation_hints": {
            "users": "10,000 monitored services across 500K hosts. 1,000 internal users querying dashboards.",
            "storage": "Metrics: 10M points/sec * 16 bytes * 86400 = 14TB/day. Logs: 1M lines/sec * 500 bytes * 86400 = 43TB/day. Total: ~57TB/day raw.",
            "bandwidth": "Metric ingestion: ~160 MB/sec. Log ingestion: ~500 MB/sec. Dashboard queries: ~10 Gbps reads at peak.",
            "qps": "Metric writes: 10M/sec. Log writes: 1M/sec. Dashboard queries: ~5K/sec. Alert evaluations: ~100K rules/30sec."
        },
        "api_design": {
            "POST /api/v1/metrics/ingest": "Batch ingest metric data points. Input: list of {metric_name, tags, value, timestamp}. High-throughput endpoint.",
            "POST /api/v1/logs/ingest": "Batch ingest log entries. Input: list of {service, level, message, timestamp, trace_id, span_id, attributes}.",
            "POST /api/v1/metrics/query": "Query metrics with PromQL-like syntax. Input: query expression, time range, step. Returns time series data.",
            "POST /api/v1/alerts/rules": "Create or update an alerting rule. Input: query, threshold, duration, severity, notification channels.",
            "GET /api/v1/traces/:traceId": "Get a full distributed trace with all spans, timings, and service hops"
        },
        "schema_design": {
            "metrics": "metric_name (varchar), tags (sorted key-value pairs, used as series key), timestamp (bigint epoch_ms), value (double). Stored in a time-series database (TimescaleDB, InfluxDB, or custom columnar store). Partitioned by time with automatic downsampling: raw data for 30 days, 1-minute aggregates for 6 months, 1-hour aggregates for 1 year.",
            "logs": "timestamp (bigint), service (varchar), level (enum), message (text), trace_id (varchar nullable), span_id (varchar nullable), attributes (jsonb). Stored in Elasticsearch or ClickHouse with full-text indexing. Partitioned by day with ILM (Index Lifecycle Management).",
            "traces": "trace_id (varchar), span_id (varchar PK), parent_span_id (varchar nullable), service (varchar), operation (varchar), start_time (bigint), duration_ms (int), status (enum), tags (jsonb). Stored in Cassandra or Elasticsearch, partitioned by trace_id.",
            "alert_rules": "id (uuid PK), name (varchar), query (text), threshold (double), comparison (enum: gt, lt, eq), duration_seconds (int), severity (enum: critical, warning, info), notification_channels (jsonb), enabled (boolean), created_by (bigint FK)"
        },
        "scaling_notes": "The ingestion pipeline is the most demanding component. Metrics arrive via a high-throughput ingest API that batches data points and writes to Kafka topics partitioned by metric name hash. Consumer groups read from Kafka and write to the time-series storage engine. For metrics, a custom columnar store or TimescaleDB handles the write throughput by partitioning data by time (1-hour chunks) and using compression (delta-of-delta for timestamps, XOR for values - the Gorilla encoding). A downsampling pipeline runs continuously, computing 1-minute and 1-hour aggregates for older data. Logs are ingested similarly via Kafka into Elasticsearch or ClickHouse, partitioned by day with automatic index rollover. Alerting rules are evaluated by an Alert Manager that periodically (every 30 seconds) executes each rule's query against the metrics store. If a threshold is breached for the configured duration, the Alert Manager fires notifications through configured channels (PagerDuty, Slack, email). Distributed tracing uses the OpenTelemetry protocol for collection.",
        "failure_modes": [
            "Kafka ingestion backlog: metric and log data accumulates in agent buffers; agents should drop oldest data when buffer is full (monitoring data is less critical than application data)",
            "Time-series storage overload: queries on hot metric series slow down; implement query-time limits and caching for popular dashboard panels",
            "Alert storm: a widespread outage triggers hundreds of alerts simultaneously; alert grouping and suppression reduce noise",
            "Elasticsearch cluster yellow/red: log search degrades or fails; recent logs may be available from Kafka replay",
            "Clock skew across hosts: metrics with future timestamps cause incorrect queries; reject data points more than 5 minutes in the future"
        ],
        "trade_offs": [
            "Pull-based (Prometheus) vs push-based (StatsD/Datadog) metric collection: pull simplifies discovery and prevents overwhelming the monitoring system but requires service discovery; push scales better for ephemeral workloads",
            "Raw data retention vs cost: storing full-resolution data for 30 days at 10M points/sec costs ~420TB; downsampling to 1-minute granularity reduces year-long storage by 60x",
            "ClickHouse vs Elasticsearch for logs: ClickHouse offers 10x better compression and query speed for structured logs but lacks full-text search flexibility; Elasticsearch excels at unstructured text search",
            "Centralized vs federated monitoring: centralized (single cluster) simplifies querying but creates a single point of failure and scaling bottleneck; federated (per-region) scales better but complicates cross-region queries"
        ],
        "diagram_description": "Application services emit metrics, logs, and traces through lightweight agents (OpenTelemetry Collector). Agents batch and forward data to regional Ingest Gateways, which validate and route data to Kafka topics (one for metrics, one for logs, one for traces). Metric Consumer groups read from Kafka and write to a Time-Series Database (TimescaleDB or a custom columnar store), partitioned by time. A Downsampling Worker continuously aggregates older data. Log Consumers write to an Elasticsearch/ClickHouse cluster with day-based partitioning. Trace Consumers write spans to Cassandra, indexed by trace_id. The Query Engine translates PromQL and LogQL queries into storage-specific queries for dashboards. The Alert Manager evaluates rules every 30 seconds against the metrics store and fires notifications via PagerDuty, Slack, or email. A Dashboard Service renders real-time visualizations from cached query results.",
        "order_index": 21
    },
    {
        "title": "Design CDN",
        "slug": "design-cdn",
        "difficulty": "hard",
        "category": "infrastructure",
        "description": "Design a Content Delivery Network that caches and serves static and dynamic content from edge servers close to users. The system must minimize latency, handle cache invalidation, support SSL termination, and provide analytics on cache performance.",
        "requirements": {
            "functional": [
                "Cache static content (images, CSS, JS, video segments) at edge locations",
                "Support cache invalidation (purge by URL, prefix, or tag)",
                "SSL/TLS termination at edge for HTTPS delivery",
                "Geographic routing to direct users to the nearest edge server",
                "Origin shielding to reduce load on customer origin servers",
                "Real-time analytics on cache hit rates, bandwidth, and latency per edge location"
            ],
            "non_functional": [
                "Serve cached content within 50ms for users within 200km of an edge location",
                "Global coverage: 200+ edge locations across 50+ countries",
                "99.999% availability for cached content serving",
                "Cache invalidation propagated to all edges within 5 seconds",
                "Handle 100 Tbps aggregate bandwidth across all edge locations"
            ]
        },
        "estimation_hints": {
            "users": "Serving content for 10,000 origin domains. 1 billion unique end users/day.",
            "storage": "Each edge location: 50TB SSD + 500TB HDD. 200 edges * 50TB hot = 10PB total hot cache.",
            "bandwidth": "100 Tbps aggregate. Each edge: ~500 Gbps peak. Origin pull: ~5 Tbps (5% cache miss rate).",
            "qps": "Cached content serves: 50M requests/sec globally. Cache misses (origin pulls): 2.5M/sec. Invalidation requests: ~1K/sec."
        },
        "api_design": {
            "GET /{path}": "Serve cached content. Edge checks cache, returns cached response (HIT) or pulls from origin/shield (MISS), caches, and returns.",
            "POST /api/v1/purge": "Invalidate cached content. Input: urls (list), prefix (string for wildcard purge), or tag (for tag-based purge). Propagates to all edges.",
            "POST /api/v1/origins": "Register a new origin. Input: domain, origin_url, ssl_cert, cache_rules, TTL defaults.",
            "GET /api/v1/analytics/:domain?range=24h": "Get CDN analytics: cache hit rate, bandwidth served, p50/p95/p99 latency, top URLs, geographic distribution",
            "PUT /api/v1/origins/:domain/rules": "Update cache rules for a domain: which paths to cache, TTL overrides, query string handling, header-based variations"
        },
        "schema_design": {
            "cache_entries": "In-memory and on-disk per edge server. Key: (domain, path, vary_key - derived from Vary headers). Value: HTTP response (headers + body). Stored using a two-tier cache: hot objects in memory (LRU), warm objects on SSD, cold objects on HDD. Each entry has TTL from Cache-Control headers or domain configuration.",
            "origin_configs": "domain (varchar PK), origin_url (varchar), ssl_certificate (text), cache_default_ttl (int), cache_rules (jsonb - path patterns to TTL and caching directives), created_at (timestamp). Stored in a global config database, replicated to all edges.",
            "invalidation_log": "id (uuid PK), domain (varchar), pattern (text), type (enum: url, prefix, tag), initiated_at (timestamp), completed_edges (int), total_edges (int), status (enum: propagating, completed)",
            "access_logs": "edge_location (varchar), timestamp (bigint), domain (varchar), path (varchar), status (int), cache_status (enum: hit, miss, expired, bypass), response_time_ms (int), bytes_served (bigint), client_country (varchar). Streamed to Kafka for analytics."
        },
        "scaling_notes": "Each edge server runs a high-performance reverse proxy (built on Nginx, Varnish, or a custom Rust-based server) with a multi-tier cache. Hot objects live in RAM (fastest, limited capacity), warm objects on NVMe SSD, and cold objects on spinning disk. A consistent hashing ring distributes cache entries across servers within an edge location, so adding or removing a server only remaps a fraction of entries. For cache misses, the edge pulls from a regional 'shield' server rather than the origin directly. The shield aggregates cache misses from multiple edges in a region, dramatically reducing origin load (request coalescing). Cache invalidation uses a pub/sub system: when a purge request arrives, it is published to a global invalidation channel. Each edge subscribes and processes purge operations locally. Geographic routing uses Anycast IP addresses combined with DNS-based geolocation: the same IP address is announced from all edge locations, and BGP routing naturally directs users to the nearest one. SSL certificates are deployed to all edge servers via a certificate management system that handles automatic renewal.",
        "failure_modes": [
            "Edge server failure: Anycast routing automatically redirects traffic to the next nearest edge within seconds",
            "Origin server unreachable: serve stale cached content (stale-while-error) while retrying origin connections; better to serve stale than error",
            "Cache stampede (thundering herd): when a popular cached item expires, many edges request it from origin simultaneously; request coalescing at the shield layer mitigates this",
            "SSL certificate expiration: automated renewal with 30-day advance warning; emergency fallback to a wildcard certificate",
            "Cache poisoning: a malicious origin response is cached and served to all users; implement response validation and cache key isolation per origin"
        ],
        "trade_offs": [
            "Cache hit rate vs freshness: longer TTLs increase hit rates (less origin load, lower latency) but serve staler content; short TTLs ensure freshness but increase origin load. Tag-based invalidation provides a middle ground.",
            "Anycast vs DNS-based routing: Anycast provides instant failover and simpler client configuration but routing depends on BGP, which may not always choose the truly closest edge; DNS geolocation is more controllable but has TTL-based failover delay",
            "Origin shielding vs direct origin pull: shields dramatically reduce origin load but add an extra hop for cache misses, increasing miss latency by 20-50ms",
            "Memory cache vs SSD-only: keeping hot objects in RAM provides sub-millisecond response but RAM is expensive; SSD-only is cheaper but adds 1-5ms for cache hits"
        ],
        "diagram_description": "End users are routed to the nearest Edge Location via Anycast IP routing. Each Edge Location has multiple cache servers organized in a consistent hash ring. When a request arrives, the edge server checks its local multi-tier cache (RAM, SSD, HDD). On a cache miss, it requests the content from the Regional Shield server, which acts as a shared mid-tier cache for multiple edges in the region. If the shield also misses, it pulls from the customer's Origin Server. The response is cached at both shield and edge tiers. Cache invalidation requests enter through the CDN Management API and are published to a global Pub/Sub channel that all edges subscribe to. Each edge processes purge operations locally against its cache. An SSL/TLS Manager handles certificate provisioning and deployment across all edges. Access logs stream from every edge to a centralized Kafka cluster, feeding real-time Analytics Dashboards and billing systems. A Health Monitor tracks edge server status and removes unhealthy nodes from the Anycast announcements.",
        "order_index": 22
    },
    {
        "title": "Design Ad Platform",
        "slug": "design-ad-platform",
        "difficulty": "hard",
        "category": "ml_systems",
        "description": "Design an online advertising platform that serves targeted ads in real-time, handles advertiser campaign management, conducts real-time bidding auctions, and tracks ad impressions, clicks, and conversions for billing and analytics.",
        "requirements": {
            "functional": [
                "Serve targeted ads based on user demographics, interests, and context",
                "Real-time bidding (RTB) auction for each ad impression",
                "Campaign management: create campaigns with budget, targeting, and creative assets",
                "Track impressions, clicks, and conversions with attribution",
                "Budget pacing: spread ad spend evenly across campaign duration",
                "Fraud detection: identify and filter invalid clicks and impressions"
            ],
            "non_functional": [
                "Ad serving decision within 100ms (end-to-end including RTB)",
                "Handle 1 million ad requests per second",
                "Click-through tracking latency under 50ms (redirect-based)",
                "99.9% availability for ad serving",
                "Billing accuracy within 0.1% (financial system-grade)"
            ]
        },
        "estimation_hints": {
            "users": "1B daily ad impressions. 100K active campaigns. 10K advertisers.",
            "storage": "Impression logs: 1B/day * 500 bytes = 500GB/day. Click logs: 50M/day * 300 bytes = 15GB/day. Total: ~200TB/year",
            "bandwidth": "Ad serve requests: 1M/sec * 2KB response = 2 GB/sec. RTB bid requests: 1M/sec * 1KB = 1 GB/sec outbound.",
            "qps": "Ad requests: 1M/sec. RTB auctions: 1M/sec. Click tracking: ~50K/sec. Conversion postbacks: ~5K/sec."
        },
        "api_design": {
            "GET /api/v1/ads/serve?placement=&user_id=&context=": "Request an ad for a placement. Returns winning ad creative, tracking URLs for impression and click. Must respond within 100ms.",
            "POST /api/v1/campaigns": "Create an advertising campaign. Input: name, budget_cents, daily_budget_cents, targeting (demographics, interests, geo), bid_strategy, start/end dates, creatives",
            "GET /api/v1/ads/track/impression/:impressionId": "Track an ad impression (1x1 pixel or beacon). Records impression for billing and analytics.",
            "GET /api/v1/ads/track/click/:clickId": "Track a click and redirect to advertiser landing page. Records click event.",
            "GET /api/v1/campaigns/:campaignId/analytics?range=": "Get campaign performance: impressions, clicks, CTR, conversions, spend, CPA"
        },
        "schema_design": {
            "campaigns": "id (bigint PK), advertiser_id (bigint FK), name (varchar), status (enum: draft, active, paused, completed), total_budget_cents (bigint), daily_budget_cents (bigint), spent_cents (bigint), bid_strategy (enum: cpc, cpm, cpa), max_bid_cents (int), targeting (jsonb), start_date (date), end_date (date)",
            "creatives": "id (bigint PK), campaign_id (bigint FK), type (enum: banner, video, native), asset_url (varchar), landing_url (varchar), width (int), height (int), status (enum: pending_review, approved, rejected)",
            "impressions": "id (uuid), campaign_id (bigint), creative_id (bigint), user_id (varchar), placement (varchar), bid_price_cents (int), win_price_cents (int), timestamp (bigint). Append-only, stored in ClickHouse partitioned by hour.",
            "clicks": "id (uuid), impression_id (uuid), user_id (varchar), landing_url (varchar), referrer (varchar), timestamp (bigint), ip_address (varchar), user_agent (varchar). For fraud analysis.",
            "budget_counters": "campaign_id (bigint PK), date (date), impressions (int), clicks (int), spent_cents (bigint), daily_budget_remaining_cents (bigint). Updated in near-real-time via Kafka aggregation. Cached in Redis for fast budget pacing decisions."
        },
        "scaling_notes": "The ad serving path is the most latency-sensitive. When an ad request arrives, the Ad Server performs candidate selection: it queries an inverted index of campaigns matching the user's attributes and placement. The candidate set is scored by a CTR prediction model (logistic regression or lightweight neural network running on the ad server, not a remote ML service, for latency). For RTB placements, bid requests are sent to demand-side platforms (DSPs) in parallel with a 80ms timeout. The auction (second-price or first-price) determines the winner. Budget pacing uses a token bucket per campaign, replenished every minute based on remaining budget and time. The pacing state is in Redis for cross-server consistency. Click and impression tracking events are written to Kafka and processed by a streaming pipeline (Flink) that updates budget counters, computes attribution, and runs fraud detection models. Fraud detection uses a combination of rules (IP velocity, user-agent anomalies) and ML models trained on historical fraud patterns.",
        "failure_modes": [
            "RTB timeout (DSP responds after 80ms): use the best available ad from direct campaigns; DSP bid is discarded",
            "Budget counter lag: campaign may slightly overspend between Redis updates; reconcile hourly and pause overspent campaigns",
            "Click tracking service failure: redirect still works (client follows the chain) but click is not recorded; retry via client-side beacon fallback",
            "CTR model serving failure: fall back to a simpler scoring function (bid * historical CTR); lower optimization but ads still serve",
            "Fraud spike: sudden bot traffic inflates impression counts; real-time fraud score threshold automatically filters suspicious traffic"
        ],
        "trade_offs": [
            "Serving latency vs targeting precision: running a deep ML model gives better targeting but adds 20-50ms; a lighter model (logistic regression) responds in 5ms with slightly lower accuracy",
            "Second-price vs first-price auction: second-price encourages truthful bidding but is complex with multiple exchanges; first-price is simpler but leads to bid shading strategies",
            "Real-time budget enforcement vs batch: real-time prevents overspend but requires fast shared state (Redis); batch is simpler but allows overspend between updates",
            "Click redirect vs beacon tracking: redirect tracking captures every click but adds latency to the user experience; beacon (JavaScript) is faster but can be blocked by ad blockers"
        ],
        "diagram_description": "When a publisher's page loads, an Ad Request is sent to the Ad Server through a global load balancer. The Ad Server queries the Campaign Index (an in-memory inverted index of active campaigns by targeting criteria) to find matching candidates. A CTR Prediction Model scores each candidate. For RTB placements, the Bid Manager sends parallel bid requests to connected DSPs with an 80ms timeout. The Auction Engine runs a second-price auction among bids, and the winning ad is returned to the publisher. The Ad Server checks the campaign's Budget Counter in Redis to ensure the daily budget is not exhausted. Impression and click tracking events go through dedicated Tracking Endpoints that write to Kafka. A Stream Processing pipeline (Flink) consumes events, updates budget counters, runs Fraud Detection (rules + ML model), computes attribution for conversions, and writes to ClickHouse for analytics. An Analytics API serves campaign performance dashboards from ClickHouse.",
        "order_index": 23
    },
    {
        "title": "Design Recommendation Engine",
        "slug": "design-recommendation-engine",
        "difficulty": "hard",
        "category": "ml_systems",
        "description": "Design a recommendation engine that provides personalized content, product, or media suggestions. The system must handle collaborative filtering, content-based filtering, and real-time re-ranking, serving recommendations with low latency at scale.",
        "requirements": {
            "functional": [
                "Generate personalized recommendations based on user interaction history",
                "Support collaborative filtering (users who liked X also liked Y)",
                "Support content-based filtering (items similar to what the user liked)",
                "Real-time re-ranking based on context (time, location, device)",
                "Handle cold-start for new users and new items",
                "A/B testing framework for comparing recommendation algorithms"
            ],
            "non_functional": [
                "Recommendation serving latency under 50ms",
                "Support 100 million users and 10 million items",
                "Update recommendations within 1 hour of new interaction data",
                "Handle 500K recommendation requests per second at peak",
                "Model training pipeline completes within 4 hours on full dataset"
            ]
        },
        "estimation_hints": {
            "users": "100M users, 10M items, 1B interactions/day. 500K recommendation requests/sec peak.",
            "storage": "User-item interaction matrix: 100M * 10M (sparse) ~500GB compressed. User embeddings: 100M * 256 floats * 4 bytes = 100GB. Item embeddings: 10M * 256 * 4 = 10GB.",
            "bandwidth": "Recommendation requests: 500K/sec * 2KB response = 1 GB/sec. Model updates: ~100GB pushed to serving infrastructure daily.",
            "qps": "Recommendation requests: 500K/sec. Feature lookups: 2M/sec (4 features per request). Interaction event ingestion: ~12K/sec."
        },
        "api_design": {
            "GET /api/v1/recommendations/:userId?context=&limit=20": "Get personalized recommendations. Context includes device, location, time. Returns ranked list of items with scores.",
            "POST /api/v1/interactions": "Record a user interaction. Input: user_id, item_id, interaction_type (view, click, purchase, rate), value (rating), timestamp.",
            "GET /api/v1/recommendations/similar/:itemId?limit=10": "Get items similar to a given item (content-based). Useful for 'you might also like' sections.",
            "POST /api/v1/experiments": "Create an A/B test experiment. Input: name, variants (list of model versions), traffic_split, metrics to track.",
            "GET /api/v1/recommendations/:userId/explain/:itemId": "Explain why an item was recommended (transparency). Returns contributing factors."
        },
        "schema_design": {
            "interactions": "user_id (bigint), item_id (bigint), interaction_type (varchar), value (float nullable), timestamp (bigint). Partitioned by date. The core training data. Stored in a data warehouse (BigQuery/Redshift) and Kafka for streaming.",
            "user_features": "user_id (bigint PK), embedding (float array 256), demographics (jsonb), interaction_counts (jsonb - per category), last_active (timestamp). Computed by the training pipeline, served from a Feature Store (Redis/DynamoDB).",
            "item_features": "item_id (bigint PK), embedding (float array 256), content_features (jsonb - category, tags, price, description embedding), popularity_score (float), created_at (timestamp). Updated by content processing and popularity computation.",
            "experiments": "id (uuid PK), name (varchar), status (enum: running, completed), variants (jsonb - list of {name, model_version, traffic_percent}), start_date (timestamp), end_date (timestamp nullable), results (jsonb nullable)"
        },
        "scaling_notes": "The recommendation system uses a two-stage architecture for latency and quality balance. The first stage (candidate retrieval) uses approximate nearest neighbor (ANN) search to find the top ~1,000 items similar to the user's embedding vector. This is done via a vector similarity search engine (FAISS, ScaNN, or Milvus) that indexes all item embeddings and supports sub-millisecond searches. The second stage (ranking) takes the 1,000 candidates and scores them using a more complex model that incorporates user features, item features, context (time, device), and cross-features. This ranking model runs as a lightweight inference server (TensorFlow Serving or ONNX Runtime) on GPUs. The model is trained offline in a batch pipeline (Spark + PyTorch) on the full interaction history, producing updated user and item embeddings. Embeddings are pushed to the serving infrastructure every few hours. For real-time personalization, a streaming pipeline (Kafka Streams) updates user interaction counts and recent activity features in the Feature Store within minutes of new interactions. Cold-start users receive popularity-based recommendations until enough interaction data accumulates.",
        "failure_modes": [
            "Vector search index failure: serve from a stale replica or fall back to popularity-based recommendations",
            "Ranking model inference timeout: return candidates from the retrieval stage ranked by a simple score (dot product of embeddings)",
            "Feature store (Redis) failure: use cached features from the last successful read; stale features degrade recommendation quality but do not cause errors",
            "Training pipeline failure: serving continues with the previous model version; set up monitoring on model staleness",
            "Cold-start: new users get poor recommendations; mitigate by asking onboarding preference questions or using contextual bandits"
        ],
        "trade_offs": [
            "Collaborative filtering vs content-based: collaborative filtering captures taste patterns but fails for new items (cold-start); content-based works for new items but cannot capture serendipitous preferences. A hybrid approach combines both.",
            "Batch vs real-time model updates: batch training on the full dataset produces the most accurate model but is hours stale; real-time updates capture recent behavior but may overfit to short-term trends. A layered approach uses batch for base embeddings and real-time for feature adjustments.",
            "Embedding dimension: higher dimensions (512) capture more nuance but increase storage, search latency, and training time; lower dimensions (64) are fast and compact but lose detail. 256 is a common compromise.",
            "Exploration vs exploitation: always recommending high-confidence items (exploitation) maximizes short-term engagement but creates filter bubbles; injecting some lower-confidence items (exploration) discovers user interests but risks showing irrelevant content"
        ],
        "diagram_description": "User interaction events (views, clicks, purchases) flow through Kafka to two consumers: a Batch Training Pipeline (Spark + PyTorch, runs every 6 hours) that produces user and item embedding vectors, and a Streaming Feature Pipeline (Kafka Streams) that updates real-time user features in the Feature Store (Redis). When a recommendation request arrives, the Recommendation Service first queries the Feature Store for the user's embedding and recent activity features. The Candidate Retrieval stage performs an approximate nearest neighbor search in a Vector Index (FAISS/ScaNN) to find the top 1,000 item candidates. The Ranking stage sends these candidates, along with user and item features, to an ML Inference Service (TensorFlow Serving) that scores and ranks them. The top-N ranked items are returned. An A/B Testing Layer routes requests to different model versions based on experiment configuration. An Explanation Service can trace back why each item was recommended by decomposing the model's scoring.",
        "order_index": 24
    },
    {
        "title": "Design Distributed Cache",
        "slug": "design-distributed-cache",
        "difficulty": "hard",
        "category": "infrastructure",
        "description": "Design a distributed in-memory caching system like Redis or Memcached that provides sub-millisecond data access across a cluster of nodes. The system must handle data partitioning, replication, eviction, and cluster management with high availability.",
        "requirements": {
            "functional": [
                "Key-value store with GET, SET, DELETE operations and TTL support",
                "Support multiple data types: strings, lists, sets, sorted sets, hash maps",
                "Distribute data across multiple nodes using consistent hashing",
                "Replication for fault tolerance (primary-replica model)",
                "Automatic failover when a primary node goes down",
                "Configurable eviction policies (LRU, LFU, random, TTL-based)"
            ],
            "non_functional": [
                "Read latency under 1ms for cache hits",
                "Write latency under 2ms with replication",
                "Support 100 nodes in a single cluster",
                "Handle 10 million operations per second across the cluster",
                "99.999% availability with automatic failover in under 5 seconds"
            ]
        },
        "estimation_hints": {
            "users": "100 nodes in the cluster. Serving 1,000 application instances. 10M ops/sec total.",
            "storage": "Each node: 64GB RAM. 100 nodes * 64GB = 6.4TB total cache capacity. With replication factor 2: 3.2TB effective.",
            "bandwidth": "Inter-node replication: ~2 Gbps. Client traffic: ~10 Gbps total. Cluster gossip: ~100 Mbps.",
            "qps": "10M ops/sec total. 100K ops/sec per node. GET:SET ratio = 10:1. 90% reads, 10% writes."
        },
        "api_design": {
            "GET /:key": "Retrieve the value for a key. Returns value and TTL remaining, or null if key does not exist or has expired.",
            "SET /:key": "Set a key-value pair. Input: value, ttl_seconds (optional), nx (set only if not exists), xx (set only if exists).",
            "DELETE /:key": "Delete a key. Returns whether the key existed.",
            "MGET /:keys": "Batch get multiple keys in one round trip. Keys may be on different nodes; client library fans out.",
            "INCR /:key": "Atomically increment a numeric value. Used for counters and rate limiters.",
            "HSET /:key/:field": "Set a field in a hash map. Supports HGET, HGETALL, HDEL for hash operations."
        },
        "schema_design": {
            "key_value_store": "Each node maintains an in-memory hash table mapping keys to value entries. Entry: {key (bytes), value (bytes), type (string/list/set/sorted_set/hash), ttl_epoch_ms (long, 0 for no expiry), last_accessed (epoch_ms for LRU), access_count (int for LFU), version (long for conflict detection)}.",
            "hash_ring": "Virtual node ring: each physical node is mapped to 150 virtual nodes (vnodes) on a consistent hash ring. Key routing: hash(key) mod ring_size maps to the responsible vnode, which maps to the physical node. The next N-1 distinct physical nodes on the ring hold replicas (N = replication factor).",
            "cluster_state": "Maintained via gossip protocol. Each node holds: {node_id, address, status (alive/suspect/dead), hash_ring_tokens (list of vnode positions), epoch (cluster version)}. Converges within 2 gossip rounds (seconds).",
            "replication_log": "Per-node append-only log of write operations. Format: {sequence_number, operation (SET/DEL), key, value, timestamp}. Replicas consume the log to stay in sync. Used for catch-up after network partitions."
        },
        "scaling_notes": "Data is distributed across nodes using consistent hashing with virtual nodes (vnodes). Each physical node owns ~150 positions on the hash ring. When a node is added or removed, only keys mapping to its vnode positions are redistributed - approximately 1/N of the total keys, where N is the number of nodes. Replication follows a primary-replica model: each key's primary is the first node clockwise on the ring, and replicas are the next N-1 distinct physical nodes. Writes go to the primary, which synchronously replicates to one replica (for durability) and asynchronously to the remaining replicas (for performance). Reads can be served by any replica for higher throughput, with optional read-your-writes consistency via version checks. Eviction runs locally per node: when memory reaches 90%, the configured eviction policy (LRU by default) removes keys until memory drops below 80%. For cluster management, a gossip protocol (SWIM-based) propagates membership changes and failure detection. When a primary fails, the gossip protocol detects it within 2-3 seconds, and the cluster automatically promotes the synchronous replica to primary.",
        "failure_modes": [
            "Primary node failure: synchronous replica is promoted within 5 seconds; async replicas catch up from the replication log. Brief window of unavailability for affected keys.",
            "Network partition (split brain): the partition with more nodes continues serving; the minority partition rejects writes. On healing, the minority syncs from the majority via the replication log.",
            "Hot key (single key receiving disproportionate traffic): the owning node becomes a bottleneck. Mitigation: client-side caching with short TTL, or key replication to multiple read replicas.",
            "Memory exhaustion: aggressive eviction kicks in; if eviction cannot keep up, the node starts rejecting writes. Alert on memory utilization above 85%.",
            "Cascading failure: one node fails, its load redistributes to neighbors, which may also become overloaded. Prevent via gradual traffic shifting and admission control."
        ],
        "trade_offs": [
            "Consistency vs latency: synchronous replication to all replicas guarantees consistency but adds latency proportional to the slowest replica; semi-synchronous (1 sync + N-1 async) balances durability and speed",
            "LRU vs LFU eviction: LRU evicts least recently used items (good for recency-biased workloads) but is susceptible to scan pollution; LFU evicts least frequently used items (good for popularity-biased workloads) but is slow to adapt to changing access patterns",
            "Virtual nodes vs simple hashing: virtual nodes provide more even key distribution and smoother rebalancing but add memory overhead and lookup complexity",
            "Gossip protocol vs centralized coordinator: gossip is decentralized and resilient to single-node failures but provides only eventual consistency for cluster state; a centralized coordinator (like ZooKeeper) provides strong consistency but is a single point of failure"
        ],
        "diagram_description": "Client applications connect to the cache cluster through a client library that maintains a local copy of the hash ring. The client hashes each key to determine the responsible primary node and sends the request directly (no proxy). The cluster consists of N nodes, each owning a portion of the consistent hash ring (150 virtual nodes per physical node). Write requests arrive at the primary node, which stores the value in its in-memory hash table, appends to its replication log, synchronously replicates to one designated replica (for durability), and acknowledges the client. Asynchronous replication streams the log to remaining replicas. Read requests can go to the primary or any replica depending on consistency requirements. A Gossip Protocol (SWIM) runs between all nodes, exchanging health status every second. When the gossip protocol detects a primary failure, it coordinates promotion of the synchronous replica. Each node runs an Eviction Manager that monitors memory usage and removes entries per the configured policy. A Cluster Manager handles node addition/removal, triggering key migration between nodes via the hash ring.",
        "order_index": 25
    },
]


# ======================================================================
# CODING PROBLEMS DATA (1-35)
# ======================================================================

CODING_PROBLEMS_1 = [
    # 1. Two Sum
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "difficulty": "easy",
        "category": "arrays",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."},
            {"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 6, we return [0, 1]."}
        ],
        "constraints": [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists."
        ],
        "hints": [
            "A brute force approach would check every pair - O(n^2). Can you do better?",
            "Use a hash map to store each number's index as you iterate.",
            "For each number, check if (target - number) already exists in the map."
        ],
        "solution_java": """class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[] { map.get(complement), i };
            }
            map.put(nums[i], i);
        }
        throw new IllegalArgumentException("No two sum solution");
    }
}""",
        "solution_python": """def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
        "test_cases": [
            {"input": "nums = [2,7,11,15], target = 9", "expected": "[0,1]"},
            {"input": "nums = [3,2,4], target = 6", "expected": "[1,2]"},
            {"input": "nums = [3,3], target = 6", "expected": "[0,1]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 1
    },
    # 2. Valid Parentheses
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "difficulty": "easy",
        "category": "stacks_queues",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if open brackets are closed by the same type of brackets, open brackets are closed in the correct order, and every close bracket has a corresponding open bracket.",
        "examples": [
            {"input": 's = "()"', "output": "true", "explanation": "Single pair of matching parentheses."},
            {"input": 's = "()[]{}"', "output": "true", "explanation": "All three types of brackets are properly matched."},
            {"input": 's = "(]"', "output": "false", "explanation": "Opening ( is closed by ] which is the wrong type."}
        ],
        "constraints": [
            "1 <= s.length <= 10^4",
            "s consists of parentheses only '()[]{}'.",
            "Each character is one of the six bracket types."
        ],
        "hints": [
            "Use a stack to keep track of opening brackets.",
            "When you encounter a closing bracket, check if it matches the top of the stack.",
            "At the end, the stack should be empty for a valid string."
        ],
        "solution_java": """class Solution {
    public boolean isValid(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        Map<Character, Character> map = Map.of(')', '(', '}', '{', ']', '[');
        for (char c : s.toCharArray()) {
            if (map.containsValue(c)) {
                stack.push(c);
            } else if (map.containsKey(c)) {
                if (stack.isEmpty() || stack.pop() != map.get(c)) {
                    return false;
                }
            }
        }
        return stack.isEmpty();
    }
}""",
        "solution_python": """def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0""",
        "test_cases": [
            {"input": 's = "()"', "expected": "true"},
            {"input": 's = "()[]{}"', "expected": "true"},
            {"input": 's = "(]"', "expected": "false"},
            {"input": 's = "([)]"', "expected": "false"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 2
    },
    # 3. Merge Two Sorted Lists
    {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "difficulty": "easy",
        "category": "linked_lists",
        "description": "You are given the heads of two sorted linked lists list1 and list2. Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.",
        "examples": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]", "explanation": "Merging the two sorted lists yields [1,1,2,3,4,4]."},
            {"input": "list1 = [], list2 = []", "output": "[]", "explanation": "Both lists are empty so the result is empty."},
            {"input": "list1 = [], list2 = [0]", "output": "[0]", "explanation": "One list is empty so the result is the other list."}
        ],
        "constraints": [
            "The number of nodes in both lists is in the range [0, 50].",
            "-100 <= Node.val <= 100",
            "Both list1 and list2 are sorted in non-decreasing order."
        ],
        "hints": [
            "Use a dummy head node to simplify the merge logic.",
            "Compare the current nodes of both lists and attach the smaller one.",
            "When one list is exhausted, attach the remainder of the other list."
        ],
        "solution_java": """class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode(-1);
        ListNode current = dummy;
        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                current.next = list1;
                list1 = list1.next;
            } else {
                current.next = list2;
                list2 = list2.next;
            }
            current = current.next;
        }
        current.next = (list1 != null) ? list1 : list2;
        return dummy.next;
    }
}""",
        "solution_python": """def merge_two_lists(list1, list2):
    dummy = ListNode(-1)
    current = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    current.next = list1 if list1 else list2
    return dummy.next""",
        "test_cases": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "expected": "[1,1,2,3,4,4]"},
            {"input": "list1 = [], list2 = []", "expected": "[]"},
            {"input": "list1 = [], list2 = [0]", "expected": "[0]"}
        ],
        "time_complexity": "O(n + m)",
        "space_complexity": "O(1)",
        "order_index": 3
    },
    # 4. Best Time to Buy and Sell Stock
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-to-buy-and-sell-stock",
        "difficulty": "easy",
        "category": "arrays",
        "description": "You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5", "explanation": "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5."},
            {"input": "prices = [7,6,4,3,1]", "output": "0", "explanation": "No profitable transaction is possible, so max profit is 0."}
        ],
        "constraints": [
            "1 <= prices.length <= 10^5",
            "0 <= prices[i] <= 10^4"
        ],
        "hints": [
            "Track the minimum price seen so far as you iterate.",
            "At each step, calculate the profit if you sold at the current price.",
            "Keep track of the maximum profit across all steps."
        ],
        "solution_java": """class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE;
        int maxProfit = 0;
        for (int price : prices) {
            if (price < minPrice) {
                minPrice = price;
            } else {
                maxProfit = Math.max(maxProfit, price - minPrice);
            }
        }
        return maxProfit;
    }
}""",
        "solution_python": """def max_profit(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        else:
            max_profit = max(max_profit, price - min_price)
    return max_profit""",
        "test_cases": [
            {"input": "prices = [7,1,5,3,6,4]", "expected": "5"},
            {"input": "prices = [7,6,4,3,1]", "expected": "0"},
            {"input": "prices = [2,4,1]", "expected": "2"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 4
    },
    # 5. Valid Palindrome
    {
        "title": "Valid Palindrome",
        "slug": "valid-palindrome",
        "difficulty": "easy",
        "category": "strings",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers. Given a string s, return true if it is a palindrome, or false otherwise.",
        "examples": [
            {"input": 's = "A man, a plan, a canal: Panama"', "output": "true", "explanation": "After cleaning: 'amanaplanacanalpanama' which is a palindrome."},
            {"input": 's = "race a car"', "output": "false", "explanation": "After cleaning: 'raceacar' which is not a palindrome."}
        ],
        "constraints": [
            "1 <= s.length <= 2 * 10^5",
            "s consists only of printable ASCII characters."
        ],
        "hints": [
            "Use two pointers, one at the start and one at the end.",
            "Skip non-alphanumeric characters.",
            "Compare characters case-insensitively."
        ],
        "solution_java": """class Solution {
    public boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}""",
        "solution_python": """def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True""",
        "test_cases": [
            {"input": 's = "A man, a plan, a canal: Panama"', "expected": "true"},
            {"input": 's = "race a car"', "expected": "false"},
            {"input": 's = " "', "expected": "true"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 5
    },
    # 6. Invert Binary Tree
    {
        "title": "Invert Binary Tree",
        "slug": "invert-binary-tree",
        "difficulty": "easy",
        "category": "trees",
        "description": "Given the root of a binary tree, invert the tree, and return its root. Inverting a binary tree means swapping the left and right children of every node in the tree.",
        "examples": [
            {"input": "root = [4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]", "explanation": "The tree is mirrored: left and right subtrees are swapped at every level."},
            {"input": "root = [2,1,3]", "output": "[2,3,1]", "explanation": "Left child 1 and right child 3 are swapped."}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [0, 100].",
            "-100 <= Node.val <= 100"
        ],
        "hints": [
            "Think recursively: invert the left subtree, invert the right subtree, then swap them.",
            "The base case is when the node is null.",
            "You can also solve this iteratively using a queue (BFS)."
        ],
        "solution_java": """class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;
        TreeNode temp = root.left;
        root.left = invertTree(root.right);
        root.right = invertTree(temp);
        return root;
    }
}""",
        "solution_python": """def invert_tree(root):
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root""",
        "test_cases": [
            {"input": "root = [4,2,7,1,3,6,9]", "expected": "[4,7,2,9,6,3,1]"},
            {"input": "root = [2,1,3]", "expected": "[2,3,1]"},
            {"input": "root = []", "expected": "[]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "order_index": 6
    },
    # 7. Maximum Subarray
    {
        "title": "Maximum Subarray",
        "slug": "maximum-subarray",
        "difficulty": "easy",
        "category": "arrays",
        "description": "Given an integer array nums, find the subarray with the largest sum, and return its sum. A subarray is a contiguous non-empty sequence of elements within an array.",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "The subarray [4,-1,2,1] has the largest sum 6."},
            {"input": "nums = [1]", "output": "1", "explanation": "The single element is the maximum subarray."},
            {"input": "nums = [5,4,-1,7,8]", "output": "23", "explanation": "The entire array has the largest sum 23."}
        ],
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4"
        ],
        "hints": [
            "Use Kadane's algorithm: maintain a running sum and reset when it goes negative.",
            "At each position, decide whether to extend the current subarray or start fresh.",
            "Track the global maximum as you go."
        ],
        "solution_java": """class Solution {
    public int maxSubArray(int[] nums) {
        int currentSum = nums[0];
        int maxSum = nums[0];
        for (int i = 1; i < nums.length; i++) {
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            maxSum = Math.max(maxSum, currentSum);
        }
        return maxSum;
    }
}""",
        "solution_python": """def max_sub_array(nums: list[int]) -> int:
    current_sum = max_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum""",
        "test_cases": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "expected": "6"},
            {"input": "nums = [1]", "expected": "1"},
            {"input": "nums = [5,4,-1,7,8]", "expected": "23"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 7
    },
    # 8. Contains Duplicate
    {
        "title": "Contains Duplicate",
        "slug": "contains-duplicate",
        "difficulty": "easy",
        "category": "arrays",
        "description": "Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "true", "explanation": "The element 1 appears twice."},
            {"input": "nums = [1,2,3,4]", "output": "false", "explanation": "All elements are distinct."},
            {"input": "nums = [1,1,1,3,3,4,3,2,4,2]", "output": "true", "explanation": "Multiple duplicates exist."}
        ],
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^9 <= nums[i] <= 10^9"
        ],
        "hints": [
            "A set stores only unique elements.",
            "If the set size is less than the array length, there are duplicates.",
            "You can also sort the array and check adjacent elements."
        ],
        "solution_java": """class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (!seen.add(num)) {
                return true;
            }
        }
        return false;
    }
}""",
        "solution_python": """def contains_duplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))""",
        "test_cases": [
            {"input": "nums = [1,2,3,1]", "expected": "true"},
            {"input": "nums = [1,2,3,4]", "expected": "false"},
            {"input": "nums = [1,1,1,3,3,4,3,2,4,2]", "expected": "true"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 8
    },
    # 9. Reverse Linked List
    {
        "title": "Reverse Linked List",
        "slug": "reverse-linked-list",
        "difficulty": "easy",
        "category": "linked_lists",
        "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]", "explanation": "The list is fully reversed."},
            {"input": "head = [1,2]", "output": "[2,1]", "explanation": "Two nodes are swapped."},
            {"input": "head = []", "output": "[]", "explanation": "Empty list remains empty."}
        ],
        "constraints": [
            "The number of nodes in the list is the range [0, 5000].",
            "-5000 <= Node.val <= 5000"
        ],
        "hints": [
            "Use three pointers: prev, current, and next.",
            "At each step, point the current node's next to prev.",
            "You can also solve this recursively."
        ],
        "solution_java": """class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        while (current != null) {
            ListNode next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }
        return prev;
    }
}""",
        "solution_python": """def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev""",
        "test_cases": [
            {"input": "head = [1,2,3,4,5]", "expected": "[5,4,3,2,1]"},
            {"input": "head = [1,2]", "expected": "[2,1]"},
            {"input": "head = []", "expected": "[]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 9
    },
    # 10. Valid Anagram
    {
        "title": "Valid Anagram",
        "slug": "valid-anagram",
        "difficulty": "easy",
        "category": "strings",
        "description": "Given two strings s and t, return true if t is an anagram of s, and false otherwise. An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "examples": [
            {"input": 's = "anagram", t = "nagaram"', "output": "true", "explanation": "Both strings contain the same characters with the same frequencies."},
            {"input": 's = "rat", t = "car"', "output": "false", "explanation": "The character frequencies differ between the two strings."}
        ],
        "constraints": [
            "1 <= s.length, t.length <= 5 * 10^4",
            "s and t consist of lowercase English letters."
        ],
        "hints": [
            "Count the frequency of each character in both strings.",
            "If the frequency maps are identical, they are anagrams.",
            "You can also sort both strings and compare."
        ],
        "solution_java": """class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) {
            count[s.charAt(i) - 'a']++;
            count[t.charAt(i) - 'a']--;
        }
        for (int c : count) {
            if (c != 0) return false;
        }
        return true;
    }
}""",
        "solution_python": """def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    from collections import Counter
    return Counter(s) == Counter(t)""",
        "test_cases": [
            {"input": 's = "anagram", t = "nagaram"', "expected": "true"},
            {"input": 's = "rat", t = "car"', "expected": "false"},
            {"input": 's = "a", t = "a"', "expected": "true"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 10
    },
    # 11. Binary Search
    {
        "title": "Binary Search",
        "slug": "binary-search",
        "difficulty": "easy",
        "category": "sorting_searching",
        "description": "Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1. You must write an algorithm with O(log n) runtime complexity.",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4", "explanation": "9 exists in nums and its index is 4."},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1", "explanation": "2 does not exist in nums so return -1."}
        ],
        "constraints": [
            "1 <= nums.length <= 10^4",
            "-10^4 < nums[i], target < 10^4",
            "All the integers in nums are unique.",
            "nums is sorted in ascending order."
        ],
        "hints": [
            "Use two pointers: left and right, narrowing the search range by half each time.",
            "Calculate mid as left + (right - left) / 2 to avoid overflow.",
            "Compare nums[mid] with target to decide which half to search."
        ],
        "solution_java": """class Solution {
    public int search(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return mid;
            else if (nums[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
}""",
        "solution_python": """def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
        "test_cases": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "expected": "4"},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "expected": "-1"},
            {"input": "nums = [5], target = 5", "expected": "0"}
        ],
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "order_index": 11
    },
    # 12. Climbing Stairs
    {
        "title": "Climbing Stairs",
        "slug": "climbing-stairs",
        "difficulty": "easy",
        "category": "dynamic_programming",
        "description": "You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "There are two ways: (1+1) and (2)."},
            {"input": "n = 3", "output": "3", "explanation": "There are three ways: (1+1+1), (1+2), and (2+1)."}
        ],
        "constraints": [
            "1 <= n <= 45"
        ],
        "hints": [
            "This is essentially the Fibonacci sequence.",
            "dp[i] = dp[i-1] + dp[i-2] where dp[i] is the number of ways to reach step i.",
            "You only need the last two values, so O(1) space is possible."
        ],
        "solution_java": """class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int prev2 = 1, prev1 = 2;
        for (int i = 3; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        return prev1;
    }
}""",
        "solution_python": """def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1""",
        "test_cases": [
            {"input": "n = 2", "expected": "2"},
            {"input": "n = 3", "expected": "3"},
            {"input": "n = 5", "expected": "8"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 12
    },
    # 13. Symmetric Tree
    {
        "title": "Symmetric Tree",
        "slug": "symmetric-tree",
        "difficulty": "easy",
        "category": "trees",
        "description": "Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).",
        "examples": [
            {"input": "root = [1,2,2,3,4,4,3]", "output": "true", "explanation": "The tree is symmetric around the center."},
            {"input": "root = [1,2,2,null,3,null,3]", "output": "false", "explanation": "The right subtree does not mirror the left subtree."}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [1, 1000].",
            "-100 <= Node.val <= 100"
        ],
        "hints": [
            "A tree is symmetric if the left subtree is a mirror reflection of the right subtree.",
            "Two trees are mirrors if their roots have the same value and the left subtree of one is the mirror of the right subtree of the other.",
            "Use recursion or BFS with a queue."
        ],
        "solution_java": """class Solution {
    public boolean isSymmetric(TreeNode root) {
        if (root == null) return true;
        return isMirror(root.left, root.right);
    }

    private boolean isMirror(TreeNode t1, TreeNode t2) {
        if (t1 == null && t2 == null) return true;
        if (t1 == null || t2 == null) return false;
        return t1.val == t2.val
            && isMirror(t1.left, t2.right)
            && isMirror(t1.right, t2.left);
    }
}""",
        "solution_python": """def is_symmetric(root) -> bool:
    def is_mirror(t1, t2):
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        return (t1.val == t2.val
                and is_mirror(t1.left, t2.right)
                and is_mirror(t1.right, t2.left))
    return root is None or is_mirror(root.left, root.right)""",
        "test_cases": [
            {"input": "root = [1,2,2,3,4,4,3]", "expected": "true"},
            {"input": "root = [1,2,2,null,3,null,3]", "expected": "false"},
            {"input": "root = [1]", "expected": "true"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "order_index": 13
    },
    # 14. Maximum Depth of Binary Tree
    {
        "title": "Maximum Depth of Binary Tree",
        "slug": "maximum-depth-of-binary-tree",
        "difficulty": "easy",
        "category": "trees",
        "description": "Given the root of a binary tree, return its maximum depth. A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "3", "explanation": "The longest path is 3 -> 20 -> 15 (or 7), which has 3 nodes."},
            {"input": "root = [1,null,2]", "output": "2", "explanation": "The path 1 -> 2 has 2 nodes."}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [0, 10^4].",
            "-100 <= Node.val <= 100"
        ],
        "hints": [
            "Use recursion: the depth of a tree is 1 + max(depth of left, depth of right).",
            "Base case: if the node is null, depth is 0.",
            "You can also use BFS and count levels."
        ],
        "solution_java": """class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
}""",
        "solution_python": """def max_depth(root) -> int:
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))""",
        "test_cases": [
            {"input": "root = [3,9,20,null,null,15,7]", "expected": "3"},
            {"input": "root = [1,null,2]", "expected": "2"},
            {"input": "root = []", "expected": "0"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "order_index": 14
    },
    # 15. Single Number
    {
        "title": "Single Number",
        "slug": "single-number",
        "difficulty": "easy",
        "category": "arrays",
        "description": "Given a non-empty array of integers nums, every element appears twice except for one. Find that single one. You must implement a solution with a linear runtime complexity and use only constant extra space.",
        "examples": [
            {"input": "nums = [2,2,1]", "output": "1", "explanation": "1 is the only element that appears once."},
            {"input": "nums = [4,1,2,1,2]", "output": "4", "explanation": "4 is the only element that appears once."},
            {"input": "nums = [1]", "output": "1", "explanation": "Single element array."}
        ],
        "constraints": [
            "1 <= nums.length <= 3 * 10^4",
            "-3 * 10^4 <= nums[i] <= 3 * 10^4",
            "Each element appears exactly twice except for one element which appears exactly once."
        ],
        "hints": [
            "XOR of a number with itself is 0.",
            "XOR of a number with 0 is the number itself.",
            "XOR all elements: pairs cancel out, leaving the single number."
        ],
        "solution_java": """class Solution {
    public int singleNumber(int[] nums) {
        int result = 0;
        for (int num : nums) {
            result ^= num;
        }
        return result;
    }
}""",
        "solution_python": """def single_number(nums: list[int]) -> int:
    result = 0
    for num in nums:
        result ^= num
    return result""",
        "test_cases": [
            {"input": "nums = [2,2,1]", "expected": "1"},
            {"input": "nums = [4,1,2,1,2]", "expected": "4"},
            {"input": "nums = [1]", "expected": "1"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 15
    },
    # 16. Linked List Cycle
    {
        "title": "Linked List Cycle",
        "slug": "linked-list-cycle",
        "difficulty": "easy",
        "category": "linked_lists",
        "description": "Given head, the head of a linked list, determine if the linked list has a cycle in it. There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Return true if there is a cycle, otherwise return false.",
        "examples": [
            {"input": "head = [3,2,0,-4], pos = 1", "output": "true", "explanation": "There is a cycle where the tail connects to the 1st node (0-indexed)."},
            {"input": "head = [1,2], pos = 0", "output": "true", "explanation": "There is a cycle where the tail connects to the 0th node."},
            {"input": "head = [1], pos = -1", "output": "false", "explanation": "There is no cycle in the linked list."}
        ],
        "constraints": [
            "The number of the nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
            "pos is -1 or a valid index in the linked-list."
        ],
        "hints": [
            "Use Floyd's cycle detection (tortoise and hare algorithm).",
            "Have a slow pointer move one step and a fast pointer move two steps.",
            "If they meet, there is a cycle."
        ],
        "solution_java": """class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }
}""",
        "solution_python": """def has_cycle(head) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False""",
        "test_cases": [
            {"input": "head = [3,2,0,-4], pos = 1", "expected": "true"},
            {"input": "head = [1,2], pos = 0", "expected": "true"},
            {"input": "head = [1], pos = -1", "expected": "false"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 16
    },
    # 17. Min Stack
    {
        "title": "Min Stack",
        "slug": "min-stack",
        "difficulty": "easy",
        "category": "stacks_queues",
        "description": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time. Implement the MinStack class with push(val), pop(), top(), and getMin() methods.",
        "examples": [
            {"input": 'MinStack(); push(-2); push(0); push(-3); getMin(); pop(); top(); getMin()', "output": "getMin()=-3, top()=0, getMin()=-2", "explanation": "After pushing -2, 0, -3: min is -3. After popping -3: top is 0, min is -2."},
            {"input": "MinStack(); push(1); push(2); top(); getMin()", "output": "top()=2, getMin()=1", "explanation": "Top returns the last pushed element, getMin returns the minimum."}
        ],
        "constraints": [
            "-2^31 <= val <= 2^31 - 1",
            "Methods pop, top and getMin operations will always be called on non-empty stacks.",
            "At most 3 * 10^4 calls will be made to push, pop, top, and getMin."
        ],
        "hints": [
            "Use two stacks: one for values and one for tracking minimums.",
            "When pushing, also push to the min stack if the value is less than or equal to the current min.",
            "Alternatively, store (value, current_min) pairs in a single stack."
        ],
        "solution_java": """class MinStack {
    private Deque<int[]> stack;

    public MinStack() {
        stack = new ArrayDeque<>();
    }

    public void push(int val) {
        int min = stack.isEmpty() ? val : Math.min(val, stack.peek()[1]);
        stack.push(new int[] { val, min });
    }

    public void pop() {
        stack.pop();
    }

    public int top() {
        return stack.peek()[0];
    }

    public int getMin() {
        return stack.peek()[1];
    }
}""",
        "solution_python": """class MinStack:
    def __init__(self):
        self.stack = []  # stores (value, current_min)

    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def get_min(self) -> int:
        return self.stack[-1][1]""",
        "test_cases": [
            {"input": "push(-2), push(0), push(-3), getMin()", "expected": "-3"},
            {"input": "push(-2), push(0), push(-3), pop(), getMin()", "expected": "-2"},
            {"input": "push(1), push(2), top()", "expected": "2"}
        ],
        "time_complexity": "O(1)",
        "space_complexity": "O(n)",
        "order_index": 17
    },
    # 18. Intersection of Two Linked Lists
    {
        "title": "Intersection of Two Linked Lists",
        "slug": "intersection-of-two-linked-lists",
        "difficulty": "easy",
        "category": "linked_lists",
        "description": "Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return null. The linked lists must retain their original structure after the function returns.",
        "examples": [
            {"input": "listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], intersectVal = 8", "output": "Intersected at '8'", "explanation": "The intersected node's value is 8. From headA: 4->1->8->4->5, from headB: 5->6->1->8->4->5."},
            {"input": "listA = [2,6,4], listB = [1,5], intersectVal = 0", "output": "null", "explanation": "The two lists do not intersect."}
        ],
        "constraints": [
            "The number of nodes of listA is in the m.",
            "The number of nodes of listB is in the n.",
            "1 <= m, n <= 3 * 10^4",
            "-10^5 <= Node.val <= 10^5"
        ],
        "hints": [
            "Use two pointers, one starting at each head.",
            "When a pointer reaches the end, redirect it to the head of the other list.",
            "They will meet at the intersection point or both reach null."
        ],
        "solution_java": """class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode a = headA, b = headB;
        while (a != b) {
            a = (a != null) ? a.next : headB;
            b = (b != null) ? b.next : headA;
        }
        return a;
    }
}""",
        "solution_python": """def get_intersection_node(headA, headB):
    a, b = headA, headB
    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a""",
        "test_cases": [
            {"input": "listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skip=2,3", "expected": "8"},
            {"input": "listA = [2,6,4], listB = [1,5], skip=3,2", "expected": "null"},
            {"input": "listA = [1,9,1,2,4], listB = [3,2,4], skip=3,1", "expected": "2"}
        ],
        "time_complexity": "O(m + n)",
        "space_complexity": "O(1)",
        "order_index": 18
    },
    # 19. Majority Element
    {
        "title": "Majority Element",
        "slug": "majority-element",
        "difficulty": "easy",
        "category": "arrays",
        "description": "Given an array nums of size n, return the majority element. The majority element is the element that appears more than n/2 times. You may assume that the majority element always exists in the array.",
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3", "explanation": "3 appears 2 times out of 3 elements."},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2", "explanation": "2 appears 4 times out of 7 elements."}
        ],
        "constraints": [
            "n == nums.length",
            "1 <= n <= 5 * 10^4",
            "-10^9 <= nums[i] <= 10^9"
        ],
        "hints": [
            "Boyer-Moore Voting Algorithm achieves O(1) space.",
            "Maintain a candidate and a count. Increment count for the same element, decrement for different.",
            "When count reaches 0, pick a new candidate."
        ],
        "solution_java": """class Solution {
    public int majorityElement(int[] nums) {
        int candidate = nums[0], count = 1;
        for (int i = 1; i < nums.length; i++) {
            if (count == 0) {
                candidate = nums[i];
                count = 1;
            } else if (nums[i] == candidate) {
                count++;
            } else {
                count--;
            }
        }
        return candidate;
    }
}""",
        "solution_python": """def majority_element(nums: list[int]) -> int:
    candidate, count = nums[0], 1
    for num in nums[1:]:
        if count == 0:
            candidate, count = num, 1
        elif num == candidate:
            count += 1
        else:
            count -= 1
    return candidate""",
        "test_cases": [
            {"input": "nums = [3,2,3]", "expected": "3"},
            {"input": "nums = [2,2,1,1,1,2,2]", "expected": "2"},
            {"input": "nums = [1]", "expected": "1"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 19
    },
    # 20. Move Zeroes
    {
        "title": "Move Zeroes",
        "slug": "move-zeroes",
        "difficulty": "easy",
        "category": "arrays",
        "description": "Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements. Note that you must do this in-place without making a copy of the array.",
        "examples": [
            {"input": "nums = [0,1,0,3,12]", "output": "[1,3,12,0,0]", "explanation": "Non-zero elements maintain order: 1, 3, 12. Zeros moved to end."},
            {"input": "nums = [0]", "output": "[0]", "explanation": "Single zero stays in place."}
        ],
        "constraints": [
            "1 <= nums.length <= 10^4",
            "-2^31 <= nums[i] <= 2^31 - 1"
        ],
        "hints": [
            "Use a write pointer that tracks where the next non-zero should go.",
            "Iterate through the array, moving non-zero elements to the write pointer position.",
            "Fill remaining positions with zeros."
        ],
        "solution_java": """class Solution {
    public void moveZeroes(int[] nums) {
        int writeIdx = 0;
        for (int num : nums) {
            if (num != 0) {
                nums[writeIdx++] = num;
            }
        }
        while (writeIdx < nums.length) {
            nums[writeIdx++] = 0;
        }
    }
}""",
        "solution_python": """def move_zeroes(nums: list[int]) -> None:
    write_idx = 0
    for num in nums:
        if num != 0:
            nums[write_idx] = num
            write_idx += 1
    for i in range(write_idx, len(nums)):
        nums[i] = 0""",
        "test_cases": [
            {"input": "nums = [0,1,0,3,12]", "expected": "[1,3,12,0,0]"},
            {"input": "nums = [0]", "expected": "[0]"},
            {"input": "nums = [1,0,0,2,3]", "expected": "[1,2,3,0,0]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 20
    },
    # 21. Container With Most Water
    {
        "title": "Container With Most Water",
        "slug": "container-with-most-water",
        "difficulty": "medium",
        "category": "arrays",
        "description": "You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]). Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.",
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49", "explanation": "Lines at index 1 (height=8) and index 8 (height=7) form a container with area min(8,7)*7 = 49."},
            {"input": "height = [1,1]", "output": "1", "explanation": "The only container has area min(1,1)*1 = 1."}
        ],
        "constraints": [
            "n == height.length",
            "2 <= n <= 10^5",
            "0 <= height[i] <= 10^4"
        ],
        "hints": [
            "Use two pointers starting at both ends of the array.",
            "The area is determined by the shorter line and the distance between lines.",
            "Move the pointer pointing to the shorter line inward to potentially find a taller line."
        ],
        "solution_java": """class Solution {
    public int maxArea(int[] height) {
        int left = 0, right = height.length - 1;
        int maxWater = 0;
        while (left < right) {
            int water = Math.min(height[left], height[right]) * (right - left);
            maxWater = Math.max(maxWater, water);
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return maxWater;
    }
}""",
        "solution_python": """def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water""",
        "test_cases": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "expected": "49"},
            {"input": "height = [1,1]", "expected": "1"},
            {"input": "height = [4,3,2,1,4]", "expected": "16"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 21
    },
    # 22. Longest Substring Without Repeating Characters
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "difficulty": "medium",
        "category": "strings",
        "description": "Given a string s, find the length of the longest substring without repeating characters.",
        "examples": [
            {"input": 's = "abcabcbb"', "output": "3", "explanation": "The longest substring without repeating characters is 'abc', with length 3."},
            {"input": 's = "bbbbb"', "output": "1", "explanation": "The longest substring is 'b', with length 1."},
            {"input": 's = "pwwkew"', "output": "3", "explanation": "The longest substring is 'wke', with length 3."}
        ],
        "constraints": [
            "0 <= s.length <= 5 * 10^4",
            "s consists of English letters, digits, symbols and spaces."
        ],
        "hints": [
            "Use a sliding window approach with two pointers.",
            "Use a set or hash map to track characters in the current window.",
            "When a duplicate is found, shrink the window from the left."
        ],
        "solution_java": """class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> map = new HashMap<>();
        int maxLen = 0, left = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (map.containsKey(c)) {
                left = Math.max(left, map.get(c) + 1);
            }
            map.put(c, right);
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}""",
        "solution_python": """def length_of_longest_substring(s: str) -> int:
    char_index = {}
    max_len = left = 0
    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len""",
        "test_cases": [
            {"input": 's = "abcabcbb"', "expected": "3"},
            {"input": 's = "bbbbb"', "expected": "1"},
            {"input": 's = "pwwkew"', "expected": "3"},
            {"input": 's = ""', "expected": "0"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(min(m, n))",
        "order_index": 22
    },
    # 23. 3Sum
    {
        "title": "3Sum",
        "slug": "3sum",
        "difficulty": "medium",
        "category": "arrays",
        "description": "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0. The solution set must not contain duplicate triplets.",
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explanation": "The distinct triplets that sum to zero are [-1,-1,2] and [-1,0,1]."},
            {"input": "nums = [0,1,1]", "output": "[]", "explanation": "No triplet sums to zero."},
            {"input": "nums = [0,0,0]", "output": "[[0,0,0]]", "explanation": "The only triplet sums to zero."}
        ],
        "constraints": [
            "3 <= nums.length <= 3000",
            "-10^5 <= nums[i] <= 10^5"
        ],
        "hints": [
            "Sort the array first, then fix one element and use two pointers for the remaining two.",
            "Skip duplicate values to avoid duplicate triplets.",
            "If nums[i] > 0, break early since no three positive numbers can sum to zero."
        ],
        "solution_java": """class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(nums);
        for (int i = 0; i < nums.length - 2; i++) {
            if (nums[i] > 0) break;
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int left = i + 1, right = nums.length - 1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;
                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        return result;
    }
}""",
        "solution_python": """def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result""",
        "test_cases": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "expected": "[[-1,-1,2],[-1,0,1]]"},
            {"input": "nums = [0,1,1]", "expected": "[]"},
            {"input": "nums = [0,0,0]", "expected": "[[0,0,0]]"}
        ],
        "time_complexity": "O(n^2)",
        "space_complexity": "O(1)",
        "order_index": 23
    },
    # 24. Group Anagrams
    {
        "title": "Group Anagrams",
        "slug": "group-anagrams",
        "difficulty": "medium",
        "category": "hash_maps",
        "description": "Given an array of strings strs, group the anagrams together. You can return the answer in any order. An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "examples": [
            {"input": 'strs = ["eat","tea","tan","ate","nat","bat"]', "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]', "explanation": "The anagram groups are: eat/tea/ate, tan/nat, and bat."},
            {"input": 'strs = [""]', "output": '[[""]]', "explanation": "Single empty string forms its own group."},
            {"input": 'strs = ["a"]', "output": '[["a"]]', "explanation": "Single character forms its own group."}
        ],
        "constraints": [
            "1 <= strs.length <= 10^4",
            "0 <= strs[i].length <= 100",
            "strs[i] consists of lowercase English letters."
        ],
        "hints": [
            "Two strings are anagrams if their sorted versions are identical.",
            "Use a hash map where the key is the sorted string and the value is the list of anagrams.",
            "Alternatively, use a character frequency tuple as the key."
        ],
        "solution_java": """class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            String key = new String(chars);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(map.values());
    }
}""",
        "solution_python": """def group_anagrams(strs: list[str]) -> list[list[str]]:
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())""",
        "test_cases": [
            {"input": 'strs = ["eat","tea","tan","ate","nat","bat"]', "expected": '[["eat","tea","ate"],["tan","nat"],["bat"]]'},
            {"input": 'strs = [""]', "expected": '[[""]]'},
            {"input": 'strs = ["a"]', "expected": '[["a"]]'}
        ],
        "time_complexity": "O(n * k log k)",
        "space_complexity": "O(n * k)",
        "order_index": 24
    },
    # 25. Merge Intervals
    {
        "title": "Merge Intervals",
        "slug": "merge-intervals",
        "difficulty": "medium",
        "category": "sorting_searching",
        "description": "Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.",
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "Intervals [1,3] and [2,6] overlap, so they are merged into [1,6]."},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]", "explanation": "Intervals [1,4] and [4,5] are considered overlapping since they share endpoint 4."}
        ],
        "constraints": [
            "1 <= intervals.length <= 10^4",
            "intervals[i].length == 2",
            "0 <= starti <= endi <= 10^4"
        ],
        "hints": [
            "Sort intervals by start time.",
            "Iterate and merge: if current interval overlaps with the last merged one, extend the end.",
            "Otherwise, add the current interval as a new entry."
        ],
        "solution_java": """class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
        List<int[]> merged = new ArrayList<>();
        for (int[] interval : intervals) {
            if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < interval[0]) {
                merged.add(interval);
            } else {
                merged.get(merged.size() - 1)[1] =
                    Math.max(merged.get(merged.size() - 1)[1], interval[1]);
            }
        }
        return merged.toArray(new int[merged.size()][]);
    }
}""",
        "solution_python": """def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged""",
        "test_cases": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "expected": "[[1,6],[8,10],[15,18]]"},
            {"input": "intervals = [[1,4],[4,5]]", "expected": "[[1,5]]"},
            {"input": "intervals = [[1,4],[0,4]]", "expected": "[[0,4]]"}
        ],
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "order_index": 25
    },
    # 26. Product of Array Except Self
    {
        "title": "Product of Array Except Self",
        "slug": "product-of-array-except-self",
        "difficulty": "medium",
        "category": "arrays",
        "description": "Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i]. The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer. You must write an algorithm that runs in O(n) time and without using the division operation.",
        "examples": [
            {"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]", "explanation": "For index 0: 2*3*4=24, index 1: 1*3*4=12, index 2: 1*2*4=8, index 3: 1*2*3=6."},
            {"input": "nums = [-1,1,0,-3,3]", "output": "[0,0,9,0,0]", "explanation": "Zero at index 2 makes all products zero except the one at index 2."}
        ],
        "constraints": [
            "2 <= nums.length <= 10^5",
            "-30 <= nums[i] <= 30",
            "The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer."
        ],
        "hints": [
            "Build prefix products from left to right.",
            "Build suffix products from right to left.",
            "answer[i] = prefix[i] * suffix[i]. You can do this in-place with O(1) extra space."
        ],
        "solution_java": """class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] answer = new int[n];
        answer[0] = 1;
        for (int i = 1; i < n; i++) {
            answer[i] = answer[i - 1] * nums[i - 1];
        }
        int suffix = 1;
        for (int i = n - 1; i >= 0; i--) {
            answer[i] *= suffix;
            suffix *= nums[i];
        }
        return answer;
    }
}""",
        "solution_python": """def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [1] * n
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer""",
        "test_cases": [
            {"input": "nums = [1,2,3,4]", "expected": "[24,12,8,6]"},
            {"input": "nums = [-1,1,0,-3,3]", "expected": "[0,0,9,0,0]"},
            {"input": "nums = [2,3]", "expected": "[3,2]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 26
    },
    # 27. Validate Binary Search Tree
    {
        "title": "Validate Binary Search Tree",
        "slug": "validate-binary-search-tree",
        "difficulty": "medium",
        "category": "trees",
        "description": "Given the root of a binary tree, determine if it is a valid binary search tree (BST). A valid BST is defined as follows: the left subtree of a node contains only nodes with keys less than the node's key, the right subtree only nodes with keys greater than the node's key, and both subtrees must also be valid BSTs.",
        "examples": [
            {"input": "root = [2,1,3]", "output": "true", "explanation": "Left child 1 < root 2 < right child 3, so it is a valid BST."},
            {"input": "root = [5,1,4,null,null,3,6]", "output": "false", "explanation": "The right child 4 is less than root 5, but 3 in 4's left subtree is less than 4 but also less than 5 which violates BST."}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [1, 10^4].",
            "-2^31 <= Node.val <= 2^31 - 1"
        ],
        "hints": [
            "Pass down the valid range (min, max) for each node.",
            "For each node, its value must be within the allowed range.",
            "Alternatively, do an in-order traversal and check that values are strictly increasing."
        ],
        "solution_java": """class Solution {
    public boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private boolean validate(TreeNode node, long min, long max) {
        if (node == null) return true;
        if (node.val <= min || node.val >= max) return false;
        return validate(node.left, min, node.val)
            && validate(node.right, node.val, max);
    }
}""",
        "solution_python": """def is_valid_bst(root) -> bool:
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node:
            return True
        if node.val <= low or node.val >= high:
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
    return validate(root)""",
        "test_cases": [
            {"input": "root = [2,1,3]", "expected": "true"},
            {"input": "root = [5,1,4,null,null,3,6]", "expected": "false"},
            {"input": "root = [1]", "expected": "true"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "order_index": 27
    },
    # 28. Number of Islands
    {
        "title": "Number of Islands",
        "slug": "number-of-islands",
        "difficulty": "medium",
        "category": "graphs",
        "description": "Given an m x n 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are surrounded by water.",
        "examples": [
            {"input": 'grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', "output": "1", "explanation": "All land cells are connected, forming one island."},
            {"input": 'grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', "output": "3", "explanation": "Three separate groups of connected land cells."}
        ],
        "constraints": [
            "m == grid.length",
            "n == grid[i].length",
            "1 <= m, n <= 300",
            "grid[i][j] is '0' or '1'."
        ],
        "hints": [
            "Use DFS or BFS to explore and mark connected land cells.",
            "When you find an unvisited '1', increment the island count and explore all connected '1's.",
            "Mark visited cells by changing '1' to '0' (or use a visited set)."
        ],
        "solution_java": """class Solution {
    public int numIslands(char[][] grid) {
        int count = 0;
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[0].length; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j);
                }
            }
        }
        return count;
    }

    private void dfs(char[][] grid, int i, int j) {
        if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || grid[i][j] == '0') {
            return;
        }
        grid[i][j] = '0';
        dfs(grid, i + 1, j);
        dfs(grid, i - 1, j);
        dfs(grid, i, j + 1);
        dfs(grid, i, j - 1);
    }
}""",
        "solution_python": """def num_islands(grid: list[list[str]]) -> int:
    def dfs(i, j):
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0':
            return
        grid[i][j] = '0'
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)

    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    return count""",
        "test_cases": [
            {"input": 'grid = [["1","1","1"],["0","1","0"],["1","1","1"]]', "expected": "1"},
            {"input": 'grid = [["1","0","1"],["0","0","0"],["1","0","1"]]', "expected": "4"},
            {"input": 'grid = [["1","1"],["1","1"]]', "expected": "1"}
        ],
        "time_complexity": "O(m * n)",
        "space_complexity": "O(m * n)",
        "order_index": 28
    },
    # 29. Course Schedule
    {
        "title": "Course Schedule",
        "slug": "course-schedule",
        "difficulty": "medium",
        "category": "graphs",
        "description": "There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai. Return true if you can finish all courses. Otherwise, return false.",
        "examples": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "true", "explanation": "Take course 0 first, then course 1. No cycle exists."},
            {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "output": "false", "explanation": "Course 0 requires 1, and course 1 requires 0. This forms a cycle."}
        ],
        "constraints": [
            "1 <= numCourses <= 2000",
            "0 <= prerequisites.length <= 5000",
            "prerequisites[i].length == 2",
            "0 <= ai, bi < numCourses"
        ],
        "hints": [
            "This is a cycle detection problem in a directed graph.",
            "Use topological sort (BFS with Kahn's algorithm or DFS with coloring).",
            "If all courses can be topologically sorted, there is no cycle."
        ],
        "solution_java": """class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        int[] inDegree = new int[numCourses];
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        for (int[] pre : prerequisites) {
            adj.get(pre[1]).add(pre[0]);
            inDegree[pre[0]]++;
        }
        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) queue.offer(i);
        }
        int count = 0;
        while (!queue.isEmpty()) {
            int course = queue.poll();
            count++;
            for (int next : adj.get(course)) {
                if (--inDegree[next] == 0) queue.offer(next);
            }
        }
        return count == numCourses;
    }
}""",
        "solution_python": """def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    from collections import deque, defaultdict
    in_degree = [0] * num_courses
    adj = defaultdict(list)
    for course, pre in prerequisites:
        adj[pre].append(course)
        in_degree[course] += 1
    queue = deque(i for i in range(num_courses) if in_degree[i] == 0)
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return count == num_courses""",
        "test_cases": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "expected": "true"},
            {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "expected": "false"},
            {"input": "numCourses = 3, prerequisites = [[1,0],[2,1]]", "expected": "true"}
        ],
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V + E)",
        "order_index": 29
    },
    # 30. Coin Change
    {
        "title": "Coin Change",
        "slug": "coin-change",
        "difficulty": "medium",
        "category": "dynamic_programming",
        "description": "You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1. You may assume that you have an infinite number of each kind of coin.",
        "examples": [
            {"input": "coins = [1,5,10,25], amount = 30", "output": "2", "explanation": "30 = 25 + 5, which uses 2 coins."},
            {"input": "coins = [2], amount = 3", "output": "-1", "explanation": "3 cannot be made from coins of denomination 2."},
            {"input": "coins = [1], amount = 0", "output": "0", "explanation": "No coins needed for amount 0."}
        ],
        "constraints": [
            "1 <= coins.length <= 12",
            "1 <= coins[i] <= 2^31 - 1",
            "0 <= amount <= 10^4"
        ],
        "hints": [
            "Use bottom-up dynamic programming.",
            "dp[i] represents the minimum number of coins to make amount i.",
            "For each amount, try every coin and take the minimum."
        ],
        "solution_java": """class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
}""",
        "solution_python": """def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1""",
        "test_cases": [
            {"input": "coins = [1,5,10,25], amount = 30", "expected": "2"},
            {"input": "coins = [2], amount = 3", "expected": "-1"},
            {"input": "coins = [1], amount = 0", "expected": "0"}
        ],
        "time_complexity": "O(amount * n)",
        "space_complexity": "O(amount)",
        "order_index": 30
    },
    # 31. Word Break
    {
        "title": "Word Break",
        "slug": "word-break",
        "difficulty": "medium",
        "category": "dynamic_programming",
        "description": "Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words. Note that the same word in the dictionary may be reused multiple times in the segmentation.",
        "examples": [
            {"input": 's = "leetcode", wordDict = ["leet","code"]', "output": "true", "explanation": "'leetcode' can be segmented as 'leet code'."},
            {"input": 's = "applepenapple", wordDict = ["apple","pen"]', "output": "true", "explanation": "'applepenapple' can be segmented as 'apple pen apple'."},
            {"input": 's = "catsandog", wordDict = ["cats","dog","sand","and","cat"]', "output": "false", "explanation": "No valid segmentation exists."}
        ],
        "constraints": [
            "1 <= s.length <= 300",
            "1 <= wordDict.length <= 1000",
            "1 <= wordDict[i].length <= 20",
            "s and wordDict[i] consist of only lowercase English letters."
        ],
        "hints": [
            "Use dynamic programming where dp[i] means s[0:i] can be segmented.",
            "For each position i, check all words in the dictionary that could end at position i.",
            "dp[i] = true if dp[i - len(word)] is true and s[i-len(word):i] == word."
        ],
        "solution_java": """class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> wordSet = new HashSet<>(wordDict);
        boolean[] dp = new boolean[s.length() + 1];
        dp[0] = true;
        for (int i = 1; i <= s.length(); i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && wordSet.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[s.length()];
    }
}""",
        "solution_python": """def word_break(s: str, word_dict: list[str]) -> bool:
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[len(s)]""",
        "test_cases": [
            {"input": 's = "leetcode", wordDict = ["leet","code"]', "expected": "true"},
            {"input": 's = "applepenapple", wordDict = ["apple","pen"]', "expected": "true"},
            {"input": 's = "catsandog", wordDict = ["cats","dog","sand","and","cat"]', "expected": "false"}
        ],
        "time_complexity": "O(n^2 * m)",
        "space_complexity": "O(n)",
        "order_index": 31
    },
    # 32. Rotate Image
    {
        "title": "Rotate Image",
        "slug": "rotate-image",
        "difficulty": "medium",
        "category": "arrays",
        "description": "You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees clockwise. You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. Do not allocate another 2D matrix.",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[[7,4,1],[8,5,2],[9,6,3]]", "explanation": "The matrix is rotated 90 degrees clockwise."},
            {"input": "matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]", "output": "[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]", "explanation": "4x4 matrix rotated 90 degrees clockwise."}
        ],
        "constraints": [
            "n == matrix.length == matrix[i].length",
            "1 <= n <= 20",
            "-1000 <= matrix[i][j] <= 1000"
        ],
        "hints": [
            "Rotate = Transpose + Reverse each row.",
            "Transpose: swap matrix[i][j] with matrix[j][i].",
            "Then reverse each row in-place."
        ],
        "solution_java": """class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        // Transpose
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = temp;
            }
        }
        // Reverse each row
        for (int i = 0; i < n; i++) {
            int left = 0, right = n - 1;
            while (left < right) {
                int temp = matrix[i][left];
                matrix[i][left] = matrix[i][right];
                matrix[i][right] = temp;
                left++;
                right--;
            }
        }
    }
}""",
        "solution_python": """def rotate(matrix: list[list[int]]) -> None:
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse each row
    for row in matrix:
        row.reverse()""",
        "test_cases": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "expected": "[[7,4,1],[8,5,2],[9,6,3]]"},
            {"input": "matrix = [[1,2],[3,4]]", "expected": "[[3,1],[4,2]]"},
            {"input": "matrix = [[1]]", "expected": "[[1]]"}
        ],
        "time_complexity": "O(n^2)",
        "space_complexity": "O(1)",
        "order_index": 32
    },
    # 33. Search in Rotated Sorted Array
    {
        "title": "Search in Rotated Sorted Array",
        "slug": "search-in-rotated-sorted-array",
        "difficulty": "medium",
        "category": "sorting_searching",
        "description": "There is an integer array nums sorted in ascending order (with distinct values). Prior to being passed to your function, nums is possibly rotated at an unknown pivot index. Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not. You must write an algorithm with O(log n) runtime complexity.",
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4", "explanation": "0 is found at index 4."},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "output": "-1", "explanation": "3 is not in the array."},
            {"input": "nums = [1], target = 0", "output": "-1", "explanation": "0 is not in the single-element array."}
        ],
        "constraints": [
            "1 <= nums.length <= 5000",
            "-10^4 <= nums[i] <= 10^4",
            "All values of nums are unique.",
            "nums is an ascending array that is possibly rotated."
        ],
        "hints": [
            "Use modified binary search. At each step, one half must be sorted.",
            "Determine which half is sorted, then check if the target lies in that sorted half.",
            "Narrow the search range accordingly."
        ],
        "solution_java": """class Solution {
    public int search(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return mid;
            if (nums[left] <= nums[mid]) {
                // Left half is sorted
                if (target >= nums[left] && target < nums[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else {
                // Right half is sorted
                if (target > nums[mid] && target <= nums[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }
        return -1;
    }
}""",
        "solution_python": """def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1""",
        "test_cases": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "expected": "4"},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "expected": "-1"},
            {"input": "nums = [1], target = 0", "expected": "-1"}
        ],
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "order_index": 33
    },
    # 34. Kth Smallest Element in BST
    {
        "title": "Kth Smallest Element in a BST",
        "slug": "kth-smallest-element-in-bst",
        "difficulty": "medium",
        "category": "trees",
        "description": "Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) of all the values of the nodes in the tree.",
        "examples": [
            {"input": "root = [3,1,4,null,2], k = 1", "output": "1", "explanation": "In-order traversal gives [1,2,3,4]. The 1st smallest is 1."},
            {"input": "root = [5,3,6,2,4,null,null,1], k = 3", "output": "3", "explanation": "In-order traversal gives [1,2,3,4,5,6]. The 3rd smallest is 3."}
        ],
        "constraints": [
            "The number of nodes in the tree is n.",
            "1 <= k <= n <= 10^4",
            "0 <= Node.val <= 10^4"
        ],
        "hints": [
            "In-order traversal of a BST visits nodes in ascending order.",
            "You can stop once you have visited k nodes.",
            "Use an iterative approach with a stack for O(H + k) time."
        ],
        "solution_java": """class Solution {
    public int kthSmallest(TreeNode root, int k) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode current = root;
        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            current = stack.pop();
            k--;
            if (k == 0) return current.val;
            current = current.right;
        }
        return -1;
    }
}""",
        "solution_python": """def kth_smallest(root, k: int) -> int:
    stack = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        k -= 1
        if k == 0:
            return current.val
        current = current.right
    return -1""",
        "test_cases": [
            {"input": "root = [3,1,4,null,2], k = 1", "expected": "1"},
            {"input": "root = [5,3,6,2,4,null,null,1], k = 3", "expected": "3"},
            {"input": "root = [1], k = 1", "expected": "1"}
        ],
        "time_complexity": "O(H + k)",
        "space_complexity": "O(H)",
        "order_index": 34
    },
    # 35. Top K Frequent Elements
    {
        "title": "Top K Frequent Elements",
        "slug": "top-k-frequent-elements",
        "difficulty": "medium",
        "category": "hash_maps",
        "description": "Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order. It is guaranteed that the answer is unique.",
        "examples": [
            {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]", "explanation": "1 appears 3 times, 2 appears 2 times. These are the top 2 frequent elements."},
            {"input": "nums = [1], k = 1", "output": "[1]", "explanation": "Only one element, so it is the most frequent."}
        ],
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4",
            "k is in the range [1, the number of unique elements in the array].",
            "It is guaranteed that the answer is unique."
        ],
        "hints": [
            "Count frequencies using a hash map.",
            "Use a min-heap of size k to keep the top k frequent elements.",
            "Alternatively, use bucket sort: create buckets where index = frequency."
        ],
        "solution_java": """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> countMap = new HashMap<>();
        for (int num : nums) {
            countMap.merge(num, 1, Integer::sum);
        }
        // Bucket sort
        List<Integer>[] buckets = new List[nums.length + 1];
        for (var entry : countMap.entrySet()) {
            int freq = entry.getValue();
            if (buckets[freq] == null) buckets[freq] = new ArrayList<>();
            buckets[freq].add(entry.getKey());
        }
        int[] result = new int[k];
        int idx = 0;
        for (int i = buckets.length - 1; i >= 0 && idx < k; i--) {
            if (buckets[i] != null) {
                for (int num : buckets[i]) {
                    result[idx++] = num;
                    if (idx == k) break;
                }
            }
        }
        return result;
    }
}""",
        "solution_python": """def top_k_frequent(nums: list[int], k: int) -> list[int]:
    from collections import Counter
    count = Counter(nums)
    # Bucket sort
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result""",
        "test_cases": [
            {"input": "nums = [1,1,1,2,2,3], k = 2", "expected": "[1,2]"},
            {"input": "nums = [1], k = 1", "expected": "[1]"},
            {"input": "nums = [4,4,4,3,3,2,1], k = 2", "expected": "[4,3]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 35
    },
]


# ======================================================================
# CODING PROBLEMS DATA (36-70)
# ======================================================================

CODING_PROBLEMS_2 = [
    {
        "title": "LRU Cache",
        "slug": "lru-cache",
        "difficulty": "medium",
        "category": "hash_maps",
        "description": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Implement the LRUCache class with get(key) returning the value or -1 if the key does not exist, and put(key, value) updating or inserting the value. When the cache reaches capacity, evict the least recently used key before inserting a new item. Both operations must run in O(1) average time.",
        "examples": [
            {"input": "[\"LRUCache\",\"put\",\"put\",\"get\",\"put\",\"get\",\"put\",\"get\",\"get\",\"get\"]\n[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]", "output": "[null,null,null,1,null,-1,null,-1,3,4]", "explanation": "Cache capacity is 2. After put(1,1) and put(2,2), get(1) returns 1. put(3,3) evicts key 2. get(2) returns -1. put(4,4) evicts key 1. get(1) returns -1, get(3) returns 3, get(4) returns 4."},
            {"input": "[\"LRUCache\",\"put\",\"get\"]\n[[1],[2,1],[2]]", "output": "[null,null,1]", "explanation": "Cache capacity 1. put(2,1) stores key 2 with value 1. get(2) returns 1."}
        ],
        "constraints": ["1 <= capacity <= 3000", "0 <= key <= 10^4", "0 <= value <= 10^5", "At most 2 * 10^5 calls to get and put"],
        "hints": ["Use a hash map combined with a doubly linked list.", "The hash map gives O(1) lookup, the doubly linked list gives O(1) insertion/removal to maintain access order.", "Move a node to the head on access; remove from the tail on eviction."],
        "solution_java": """import java.util.*;

class LRUCache {
    class Node {
        int key, val;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }
    private Map<Integer, Node> map = new HashMap<>();
    private Node head = new Node(0, 0), tail = new Node(0, 0);
    private int capacity;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        remove(node);
        insertHead(node);
        return node.val;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            remove(map.get(key));
        }
        if (map.size() == capacity) {
            remove(tail.prev);
        }
        insertHead(new Node(key, value));
    }

    private void remove(Node node) {
        map.remove(node.key);
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertHead(Node node) {
        map.put(node.key, node);
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
}""",
        "solution_python": """class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        del self.cache[node.key]
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_head(self, node):
        self.cache[node.key] = node
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        if len(self.cache) == self.cap:
            self._remove(self.tail.prev)
        self._insert_head(Node(key, value))""",
        "test_cases": [
            {"input": "[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]", "expected": "[null,null,null,1,null,-1,null,-1,3,4]"},
            {"input": "[[1],[2,1],[2]]", "expected": "[null,null,1]"},
            {"input": "[[2],[2,1],[1,1],[2,3],[4,1],[1],[2]]", "expected": "[null,null,null,null,-1,1,3]"}
        ],
        "time_complexity": "O(1)",
        "space_complexity": "O(capacity)",
        "order_index": 36
    },
    {
        "title": "Binary Tree Level Order Traversal",
        "slug": "binary-tree-level-order-traversal",
        "difficulty": "medium",
        "category": "trees",
        "description": "Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]", "explanation": "Level 0: [3], Level 1: [9,20], Level 2: [15,7]."},
            {"input": "root = [1]", "output": "[[1]]", "explanation": "Single node at level 0."}
        ],
        "constraints": ["0 <= number of nodes <= 2000", "-1000 <= Node.val <= 1000", "The tree may be empty"],
        "hints": ["Use BFS with a queue.", "Process all nodes at the current level before moving to the next.", "Track the number of nodes at each level using the queue size."],
        "solution_java": """import java.util.*;

class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> level = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                level.add(node.val);
                if (node.left != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
            result.add(level);
        }
        return result;
    }
}""",
        "solution_python": """from collections import deque
from typing import List, Optional

class Solution:
    def levelOrder(self, root: Optional['TreeNode']) -> List[List[int]]:
        if not root:
            return []
        result = []
        queue = deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result""",
        "test_cases": [
            {"input": "[3,9,20,null,null,15,7]", "expected": "[[3],[9,20],[15,7]]"},
            {"input": "[1]", "expected": "[[1]]"},
            {"input": "[]", "expected": "[]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 37
    },
    {
        "title": "Implement Trie (Prefix Tree)",
        "slug": "implement-trie",
        "difficulty": "medium",
        "category": "trees",
        "description": "A trie (pronounced as 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. Implement the Trie class with insert(word), search(word) returning true if the word is in the trie, and startsWith(prefix) returning true if any word starts with the given prefix.",
        "examples": [
            {"input": "[\"Trie\",\"insert\",\"search\",\"search\",\"startsWith\",\"insert\",\"search\"]\n[[],[\"apple\"],[\"apple\"],[\"app\"],[\"app\"],[\"app\"],[\"app\"]]", "output": "[null,null,true,false,true,null,true]", "explanation": "Insert 'apple', search 'apple' returns true, search 'app' returns false (not a complete word), startsWith 'app' returns true, insert 'app', now search 'app' returns true."},
            {"input": "[\"Trie\",\"insert\",\"search\",\"startsWith\"]\n[[],[\"hello\"],[\"hell\"],[\"hell\"]]", "output": "[null,null,false,true]", "explanation": "Insert 'hello'. 'hell' is not a complete word but is a prefix."}
        ],
        "constraints": ["1 <= word.length, prefix.length <= 2000", "word and prefix consist only of lowercase English letters", "At most 3 * 10^4 calls to insert, search, startsWith"],
        "hints": ["Use a tree where each node has up to 26 children (one per letter).", "Mark the end of each word with a boolean flag.", "For startsWith, traverse without requiring the end-of-word flag."],
        "solution_java": """class Trie {
    private Trie[] children = new Trie[26];
    private boolean isEnd = false;

    public Trie() {}

    public void insert(String word) {
        Trie node = this;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null)
                node.children[idx] = new Trie();
            node = node.children[idx];
        }
        node.isEnd = true;
    }

    public boolean search(String word) {
        Trie node = find(word);
        return node != null && node.isEnd;
    }

    public boolean startsWith(String prefix) {
        return find(prefix) != null;
    }

    private Trie find(String s) {
        Trie node = this;
        for (char c : s.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return null;
            node = node.children[idx];
        }
        return node;
    }
}""",
        "solution_python": """class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word: str) -> None:
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, s: str):
        node = self
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node""",
        "test_cases": [
            {"input": "[[],[\"apple\"],[\"apple\"],[\"app\"],[\"app\"],[\"app\"],[\"app\"]]", "expected": "[null,null,true,false,true,null,true]"},
            {"input": "[[],[\"hello\"],[\"hell\"],[\"hell\"]]", "expected": "[null,null,false,true]"},
            {"input": "[[],[\"a\"],[\"a\"],[\"a\"]]", "expected": "[null,null,true,true]"}
        ],
        "time_complexity": "O(m) per operation where m is word length",
        "space_complexity": "O(n * m) total",
        "order_index": 38
    },
    {
        "title": "Word Search",
        "slug": "word-search",
        "difficulty": "medium",
        "category": "backtracking",
        "description": "Given an m x n grid of characters board and a string word, return true if word exists in the grid. The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.",
        "examples": [
            {"input": "board = [[\"A\",\"B\",\"C\",\"E\"],[\"S\",\"F\",\"C\",\"S\"],[\"A\",\"D\",\"E\",\"E\"]], word = \"ABCCED\"", "output": "true", "explanation": "The word ABCCED can be found following a path from A(0,0)->B(0,1)->C(0,2)->C(1,2)->E(2,2)->D(2,1)."},
            {"input": "board = [[\"A\",\"B\",\"C\",\"E\"],[\"S\",\"F\",\"C\",\"S\"],[\"A\",\"D\",\"E\",\"E\"]], word = \"ABCB\"", "output": "false", "explanation": "The letter B at (0,1) cannot be reused."}
        ],
        "constraints": ["m == board.length", "n == board[i].length", "1 <= m, n <= 6", "1 <= word.length <= 15"],
        "hints": ["Use backtracking: try each cell as a start, then explore all four directions.", "Mark visited cells to avoid revisiting in the current path.", "Restore the cell after backtracking."],
        "solution_java": """class Solution {
    public boolean exist(char[][] board, String word) {
        int m = board.length, n = board[0].length;
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (dfs(board, word, i, j, 0)) return true;
        return false;
    }

    private boolean dfs(char[][] board, String word, int i, int j, int k) {
        if (k == word.length()) return true;
        if (i < 0 || i >= board.length || j < 0 || j >= board[0].length
            || board[i][j] != word.charAt(k)) return false;
        char tmp = board[i][j];
        board[i][j] = '#';
        boolean found = dfs(board, word, i+1, j, k+1)
                      || dfs(board, word, i-1, j, k+1)
                      || dfs(board, word, i, j+1, k+1)
                      || dfs(board, word, i, j-1, k+1);
        board[i][j] = tmp;
        return found;
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])

        def dfs(i, j, k):
            if k == len(word):
                return True
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
                return False
            tmp = board[i][j]
            board[i][j] = '#'
            found = (dfs(i+1, j, k+1) or dfs(i-1, j, k+1) or
                     dfs(i, j+1, k+1) or dfs(i, j-1, k+1))
            board[i][j] = tmp
            return found

        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False""",
        "test_cases": [
            {"input": "board = [[\"A\",\"B\",\"C\",\"E\"],[\"S\",\"F\",\"C\",\"S\"],[\"A\",\"D\",\"E\",\"E\"]], word = \"ABCCED\"", "expected": "true"},
            {"input": "board = [[\"A\",\"B\",\"C\",\"E\"],[\"S\",\"F\",\"C\",\"S\"],[\"A\",\"D\",\"E\",\"E\"]], word = \"SEE\"", "expected": "true"},
            {"input": "board = [[\"A\",\"B\",\"C\",\"E\"],[\"S\",\"F\",\"C\",\"S\"],[\"A\",\"D\",\"E\",\"E\"]], word = \"ABCB\"", "expected": "false"}
        ],
        "time_complexity": "O(m * n * 4^L)",
        "space_complexity": "O(L)",
        "order_index": 39
    },
    {
        "title": "Letter Combinations of a Phone Number",
        "slug": "letter-combinations-of-a-phone-number",
        "difficulty": "medium",
        "category": "backtracking",
        "description": "Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. The mapping is the same as on telephone buttons: 2->abc, 3->def, 4->ghi, 5->jkl, 6->mno, 7->pqrs, 8->tuv, 9->wxyz.",
        "examples": [
            {"input": "digits = \"23\"", "output": "[\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]", "explanation": "Digit 2 maps to 'abc' and digit 3 maps to 'def'. All combinations of one letter from each are generated."},
            {"input": "digits = \"\"", "output": "[]", "explanation": "Empty input yields no combinations."}
        ],
        "constraints": ["0 <= digits.length <= 4", "digits[i] is a digit in the range ['2', '9']"],
        "hints": ["Map each digit to its corresponding letters.", "Use backtracking to build combinations one letter at a time.", "The total number of combinations is the product of letter counts for each digit."],
        "solution_java": """import java.util.*;

class Solution {
    private static final String[] MAPPING = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};

    public List<String> letterCombinations(String digits) {
        List<String> result = new ArrayList<>();
        if (digits.isEmpty()) return result;
        backtrack(digits, 0, new StringBuilder(), result);
        return result;
    }

    private void backtrack(String digits, int idx, StringBuilder sb, List<String> result) {
        if (idx == digits.length()) {
            result.add(sb.toString());
            return;
        }
        for (char c : MAPPING[digits.charAt(idx) - '0'].toCharArray()) {
            sb.append(c);
            backtrack(digits, idx + 1, sb, result);
            sb.deleteCharAt(sb.length() - 1);
        }
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        mapping = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
                   '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
        result = []

        def backtrack(idx, path):
            if idx == len(digits):
                result.append(''.join(path))
                return
            for ch in mapping[digits[idx]]:
                path.append(ch)
                backtrack(idx + 1, path)
                path.pop()

        backtrack(0, [])
        return result""",
        "test_cases": [
            {"input": "\"23\"", "expected": "[\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]"},
            {"input": "\"\"", "expected": "[]"},
            {"input": "\"2\"", "expected": "[\"a\",\"b\",\"c\"]"}
        ],
        "time_complexity": "O(4^n)",
        "space_complexity": "O(n)",
        "order_index": 40
    },
    {
        "title": "Subsets",
        "slug": "subsets",
        "difficulty": "medium",
        "category": "backtracking",
        "description": "Given an integer array nums of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the subsets in any order.",
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]", "explanation": "All 2^3 = 8 subsets of {1,2,3} are returned."},
            {"input": "nums = [0]", "output": "[[],[0]]", "explanation": "Two subsets: empty set and {0}."}
        ],
        "constraints": ["1 <= nums.length <= 10", "-10 <= nums[i] <= 10", "All the numbers of nums are unique"],
        "hints": ["Each element is either included or excluded from a subset.", "Use backtracking, branching on include/exclude at each index.", "Alternatively, iterate and for each existing subset, create a new one with the current element added."],
        "solution_java": """import java.util.*;

class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), result);
        return result;
    }

    private void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
        result.add(new ArrayList<>(current));
        for (int i = start; i < nums.length; i++) {
            current.add(nums[i]);
            backtrack(nums, i + 1, current, result);
            current.remove(current.size() - 1);
        }
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []

        def backtrack(start, current):
            result.append(current[:])
            for i in range(start, len(nums)):
                current.append(nums[i])
                backtrack(i + 1, current)
                current.pop()

        backtrack(0, [])
        return result""",
        "test_cases": [
            {"input": "[1,2,3]", "expected": "[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]"},
            {"input": "[0]", "expected": "[[],[0]]"},
            {"input": "[1,2]", "expected": "[[],[1],[1,2],[2]]"}
        ],
        "time_complexity": "O(n * 2^n)",
        "space_complexity": "O(n)",
        "order_index": 41
    },
    {
        "title": "Permutations",
        "slug": "permutations",
        "difficulty": "medium",
        "category": "backtracking",
        "description": "Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.",
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]", "explanation": "All 3! = 6 permutations of [1,2,3]."},
            {"input": "nums = [0,1]", "output": "[[0,1],[1,0]]", "explanation": "Two permutations of [0,1]."}
        ],
        "constraints": ["1 <= nums.length <= 6", "-10 <= nums[i] <= 10", "All the integers of nums are unique"],
        "hints": ["Use backtracking with a visited set to track used elements.", "At each position, try every unused element.", "When the current permutation reaches the length of nums, add it to results."],
        "solution_java": """import java.util.*;

class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, new boolean[nums.length], new ArrayList<>(), result);
        return result;
    }

    private void backtrack(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
        if (current.size() == nums.length) {
            result.add(new ArrayList<>(current));
            return;
        }
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;
            used[i] = true;
            current.add(nums[i]);
            backtrack(nums, used, current, result);
            current.remove(current.size() - 1);
            used[i] = false;
        }
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []

        def backtrack(current, remaining):
            if not remaining:
                result.append(current[:])
                return
            for i in range(len(remaining)):
                current.append(remaining[i])
                backtrack(current, remaining[:i] + remaining[i+1:])
                current.pop()

        backtrack([], nums)
        return result""",
        "test_cases": [
            {"input": "[1,2,3]", "expected": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"},
            {"input": "[0,1]", "expected": "[[0,1],[1,0]]"},
            {"input": "[1]", "expected": "[[1]]"}
        ],
        "time_complexity": "O(n!)",
        "space_complexity": "O(n)",
        "order_index": 42
    },
    {
        "title": "Combination Sum",
        "slug": "combination-sum",
        "difficulty": "medium",
        "category": "backtracking",
        "description": "Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.",
        "examples": [
            {"input": "candidates = [2,3,6,7], target = 7", "output": "[[2,2,3],[7]]", "explanation": "2+2+3=7 and 7=7 are the only two combinations."},
            {"input": "candidates = [2,3,5], target = 8", "output": "[[2,2,2,2],[2,3,3],[3,5]]", "explanation": "Three combinations sum to 8."}
        ],
        "constraints": ["1 <= candidates.length <= 30", "2 <= candidates[i] <= 40", "All elements of candidates are distinct", "1 <= target <= 40"],
        "hints": ["Sort the candidates to enable pruning.", "Use backtracking, allowing repeated selection of the same element.", "Start the next recursion from the current index (not i+1) to allow reuse."],
        "solution_java": """import java.util.*;

class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(candidates);
        backtrack(candidates, target, 0, new ArrayList<>(), result);
        return result;
    }

    private void backtrack(int[] candidates, int remain, int start,
                           List<Integer> current, List<List<Integer>> result) {
        if (remain == 0) {
            result.add(new ArrayList<>(current));
            return;
        }
        for (int i = start; i < candidates.length; i++) {
            if (candidates[i] > remain) break;
            current.add(candidates[i]);
            backtrack(candidates, remain - candidates[i], i, current, result);
            current.remove(current.size() - 1);
        }
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        candidates.sort()

        def backtrack(remain, start, current):
            if remain == 0:
                result.append(current[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remain:
                    break
                current.append(candidates[i])
                backtrack(remain - candidates[i], i, current)
                current.pop()

        backtrack(target, 0, [])
        return result""",
        "test_cases": [
            {"input": "candidates = [2,3,6,7], target = 7", "expected": "[[2,2,3],[7]]"},
            {"input": "candidates = [2,3,5], target = 8", "expected": "[[2,2,2,2],[2,3,3],[3,5]]"},
            {"input": "candidates = [2], target = 1", "expected": "[]"}
        ],
        "time_complexity": "O(n^(target/min))",
        "space_complexity": "O(target/min)",
        "order_index": 43
    },
    {
        "title": "Generate Parentheses",
        "slug": "generate-parentheses",
        "difficulty": "medium",
        "category": "backtracking",
        "description": "Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.",
        "examples": [
            {"input": "n = 3", "output": "[\"((()))\",\"(()())\",\"(())()\",\"()(())\",\"()()()\"]", "explanation": "All 5 valid combinations of 3 pairs of parentheses."},
            {"input": "n = 1", "output": "[\"()\"]", "explanation": "Only one valid combination with 1 pair."}
        ],
        "constraints": ["1 <= n <= 8"],
        "hints": ["Use backtracking with counts of open and close parentheses used.", "You can add '(' if open count < n.", "You can add ')' if close count < open count."],
        "solution_java": """import java.util.*;

class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        backtrack(n, 0, 0, new StringBuilder(), result);
        return result;
    }

    private void backtrack(int n, int open, int close, StringBuilder sb, List<String> result) {
        if (sb.length() == 2 * n) {
            result.add(sb.toString());
            return;
        }
        if (open < n) {
            sb.append('(');
            backtrack(n, open + 1, close, sb, result);
            sb.deleteCharAt(sb.length() - 1);
        }
        if (close < open) {
            sb.append(')');
            backtrack(n, open, close + 1, sb, result);
            sb.deleteCharAt(sb.length() - 1);
        }
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []

        def backtrack(s, open_count, close_count):
            if len(s) == 2 * n:
                result.append(s)
                return
            if open_count < n:
                backtrack(s + '(', open_count + 1, close_count)
            if close_count < open_count:
                backtrack(s + ')', open_count, close_count + 1)

        backtrack('', 0, 0)
        return result""",
        "test_cases": [
            {"input": "3", "expected": "[\"((()))\",\"(()())\",\"(())()\",\"()(())\",\"()()()\"]"},
            {"input": "1", "expected": "[\"()\"]"},
            {"input": "2", "expected": "[\"(())\",\"()()\"]"}
        ],
        "time_complexity": "O(4^n / sqrt(n))",
        "space_complexity": "O(n)",
        "order_index": 44
    },
    {
        "title": "Decode Ways",
        "slug": "decode-ways",
        "difficulty": "medium",
        "category": "dynamic_programming",
        "description": "A message containing letters from A-Z can be encoded as numbers using the mapping: 'A' -> \"1\", 'B' -> \"2\", ..., 'Z' -> \"26\". Given a string s containing only digits, return the number of ways to decode it. For example, \"11106\" can be decoded as \"AAJF\" (1 1 10 6) or \"KJF\" (11 10 6). Note that the grouping (1 11 06) is invalid because \"06\" is not a valid code.",
        "examples": [
            {"input": "s = \"12\"", "output": "2", "explanation": "It could be decoded as 'AB' (1 2) or 'L' (12)."},
            {"input": "s = \"226\"", "output": "3", "explanation": "It could be decoded as 'BZ' (2 26), 'VF' (22 6), or 'BBF' (2 2 6)."}
        ],
        "constraints": ["1 <= s.length <= 100", "s contains only digits", "s may contain leading zeros"],
        "hints": ["Use dynamic programming where dp[i] = number of ways to decode s[0..i-1].", "A single digit 1-9 contributes dp[i-1] ways.", "A two-digit number 10-26 contributes dp[i-2] ways."],
        "solution_java": """class Solution {
    public int numDecodings(String s) {
        if (s.charAt(0) == '0') return 0;
        int n = s.length();
        int prev2 = 1, prev1 = 1;
        for (int i = 1; i < n; i++) {
            int curr = 0;
            if (s.charAt(i) != '0') curr += prev1;
            int twoDigit = Integer.parseInt(s.substring(i - 1, i + 1));
            if (twoDigit >= 10 && twoDigit <= 26) curr += prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }
}""",
        "solution_python": """class Solution:
    def numDecodings(self, s: str) -> int:
        if s[0] == '0':
            return 0
        prev2, prev1 = 1, 1
        for i in range(1, len(s)):
            curr = 0
            if s[i] != '0':
                curr += prev1
            two_digit = int(s[i-1:i+1])
            if 10 <= two_digit <= 26:
                curr += prev2
            prev2, prev1 = prev1, curr
        return prev1""",
        "test_cases": [
            {"input": "\"12\"", "expected": "2"},
            {"input": "\"226\"", "expected": "3"},
            {"input": "\"06\"", "expected": "0"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 45
    },
    {
        "title": "House Robber",
        "slug": "house-robber",
        "difficulty": "medium",
        "category": "dynamic_programming",
        "description": "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected, so if two adjacent houses are broken into on the same night the police will be alerted. Given an integer array nums representing the amount of money at each house, return the maximum amount of money you can rob tonight without alerting the police.",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "4", "explanation": "Rob house 1 (money = 1) and house 3 (money = 3). Total = 1 + 3 = 4."},
            {"input": "nums = [2,7,9,3,1]", "output": "12", "explanation": "Rob house 1 (2), house 3 (9), house 5 (1). Total = 2 + 9 + 1 = 12."}
        ],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 400"],
        "hints": ["At each house, decide to rob it (add its value to the best from two houses back) or skip it (take the best from the previous house).", "dp[i] = max(dp[i-1], dp[i-2] + nums[i]).", "You only need two variables instead of a full array."],
        "solution_java": """class Solution {
    public int rob(int[] nums) {
        int prev2 = 0, prev1 = 0;
        for (int num : nums) {
            int curr = Math.max(prev1, prev2 + num);
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        prev2, prev1 = 0, 0
        for num in nums:
            prev2, prev1 = prev1, max(prev1, prev2 + num)
        return prev1""",
        "test_cases": [
            {"input": "[1,2,3,1]", "expected": "4"},
            {"input": "[2,7,9,3,1]", "expected": "12"},
            {"input": "[2,1,1,2]", "expected": "4"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 46
    },
    {
        "title": "Longest Increasing Subsequence",
        "slug": "longest-increasing-subsequence",
        "difficulty": "medium",
        "category": "dynamic_programming",
        "description": "Given an integer array nums, return the length of the longest strictly increasing subsequence.",
        "examples": [
            {"input": "nums = [10,9,2,5,3,7,101,18]", "output": "4", "explanation": "The longest increasing subsequence is [2,3,7,101] with length 4."},
            {"input": "nums = [0,1,0,3,2,3]", "output": "4", "explanation": "The longest increasing subsequence is [0,1,2,3]."}
        ],
        "constraints": ["1 <= nums.length <= 2500", "-10^4 <= nums[i] <= 10^4"],
        "hints": ["O(n^2) DP: dp[i] = length of LIS ending at index i.", "O(n log n): maintain a tails array where tails[i] is the smallest tail element for an increasing subsequence of length i+1.", "Use binary search to find the position to update in the tails array."],
        "solution_java": """import java.util.*;

class Solution {
    public int lengthOfLIS(int[] nums) {
        List<Integer> tails = new ArrayList<>();
        for (int num : nums) {
            int pos = Collections.binarySearch(tails, num);
            if (pos < 0) pos = -(pos + 1);
            if (pos == tails.size()) tails.add(num);
            else tails.set(pos, num);
        }
        return tails.size();
    }
}""",
        "solution_python": """from typing import List
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []
        for num in nums:
            pos = bisect.bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num
        return len(tails)""",
        "test_cases": [
            {"input": "[10,9,2,5,3,7,101,18]", "expected": "4"},
            {"input": "[0,1,0,3,2,3]", "expected": "4"},
            {"input": "[7,7,7,7,7,7,7]", "expected": "1"}
        ],
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "order_index": 47
    },
    {
        "title": "Sort Colors",
        "slug": "sort-colors",
        "difficulty": "medium",
        "category": "sorting_searching",
        "description": "Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red (0), white (1), and blue (2). You must solve this problem without using the library's sort function. Can you come up with a one-pass algorithm using only constant extra space?",
        "examples": [
            {"input": "nums = [2,0,2,1,1,0]", "output": "[0,0,1,1,2,2]", "explanation": "After sorting: all 0s, then 1s, then 2s."},
            {"input": "nums = [2,0,1]", "output": "[0,1,2]", "explanation": "Sorted in one pass using the Dutch National Flag algorithm."}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 300", "nums[i] is either 0, 1, or 2"],
        "hints": ["Use the Dutch National Flag algorithm with three pointers.", "low pointer for the boundary of 0s, high pointer for the boundary of 2s, mid for traversal.", "Swap elements at mid with low or high based on their value."],
        "solution_java": """class Solution {
    public void sortColors(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1;
        while (mid <= high) {
            if (nums[mid] == 0) {
                swap(nums, low++, mid++);
            } else if (nums[mid] == 1) {
                mid++;
            } else {
                swap(nums, mid, high--);
            }
        }
    }

    private void swap(int[] nums, int i, int j) {
        int tmp = nums[i];
        nums[i] = nums[j];
        nums[j] = tmp;
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1""",
        "test_cases": [
            {"input": "[2,0,2,1,1,0]", "expected": "[0,0,1,1,2,2]"},
            {"input": "[2,0,1]", "expected": "[0,1,2]"},
            {"input": "[0]", "expected": "[0]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 48
    },
    {
        "title": "Find Minimum in Rotated Sorted Array",
        "slug": "find-minimum-in-rotated-sorted-array",
        "difficulty": "medium",
        "category": "sorting_searching",
        "description": "Suppose an array of length n sorted in ascending order is rotated between 1 and n times. Given the sorted rotated array nums of unique elements, return the minimum element. You must write an algorithm that runs in O(log n) time.",
        "examples": [
            {"input": "nums = [3,4,5,1,2]", "output": "1", "explanation": "The original sorted array [1,2,3,4,5] was rotated 3 times."},
            {"input": "nums = [4,5,6,7,0,1,2]", "output": "0", "explanation": "The original array was [0,1,2,4,5,6,7] rotated 4 times."}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 5000", "-5000 <= nums[i] <= 5000", "All values are unique"],
        "hints": ["Use binary search.", "Compare the mid element with the rightmost element to decide which half contains the minimum.", "If nums[mid] > nums[right], the minimum is in the right half."],
        "solution_java": """class Solution {
    public int findMin(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi]) lo = mid + 1;
            else hi = mid;
        }
        return nums[lo];
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1
            else:
                hi = mid
        return nums[lo]""",
        "test_cases": [
            {"input": "[3,4,5,1,2]", "expected": "1"},
            {"input": "[4,5,6,7,0,1,2]", "expected": "0"},
            {"input": "[11,13,15,17]", "expected": "11"}
        ],
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "order_index": 49
    },
    {
        "title": "Kth Largest Element in an Array",
        "slug": "kth-largest-element-in-an-array",
        "difficulty": "medium",
        "category": "sorting_searching",
        "description": "Given an integer array nums and an integer k, return the kth largest element in the array. Note that it is the kth largest element in the sorted order, not the kth distinct element. Can you solve it without sorting?",
        "examples": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5", "explanation": "Sorted: [1,2,3,4,5,6]. The 2nd largest is 5."},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "4", "explanation": "Sorted: [1,2,2,3,3,4,5,5,6]. The 4th largest is 4."}
        ],
        "constraints": ["1 <= k <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "hints": ["Use a min-heap of size k to find the kth largest efficiently.", "Alternatively, use Quickselect (average O(n) time).", "A min-heap approach: push elements, pop when size > k, the top is the kth largest."],
        "solution_java": """import java.util.PriorityQueue;

class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) minHeap.poll();
        }
        return minHeap.peek();
    }
}""",
        "solution_python": """import heapq
from typing import List

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]""",
        "test_cases": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "expected": "5"},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "expected": "4"},
            {"input": "nums = [1], k = 1", "expected": "1"}
        ],
        "time_complexity": "O(n log k)",
        "space_complexity": "O(k)",
        "order_index": 50
    },
    {
        "title": "Daily Temperatures",
        "slug": "daily-temperatures",
        "difficulty": "medium",
        "category": "stacks_queues",
        "description": "Given an array of integers temperatures representing the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0.",
        "examples": [
            {"input": "temperatures = [73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]", "explanation": "For day 0 (73), the next warmer day is day 1 (74), so answer[0]=1. For day 2 (75), the next warmer is day 6 (76), so answer[2]=4."},
            {"input": "temperatures = [30,40,50,60]", "output": "[1,1,1,0]", "explanation": "Each day's next warmer temperature is the next day, except the last."}
        ],
        "constraints": ["1 <= temperatures.length <= 10^5", "30 <= temperatures[i] <= 100"],
        "hints": ["Use a monotonic decreasing stack of indices.", "When a warmer temperature is found, pop all indices from the stack that have a lower temperature.", "The difference between current index and popped index is the answer for the popped index."],
        "solution_java": """import java.util.Stack;

class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] answer = new int[n];
        Stack<Integer> stack = new Stack<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int idx = stack.pop();
                answer[idx] = i - idx;
            }
            stack.push(i);
        }
        return answer;
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = []
        for i in range(n):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                idx = stack.pop()
                answer[idx] = i - idx
            stack.append(i)
        return answer""",
        "test_cases": [
            {"input": "[73,74,75,71,69,72,76,73]", "expected": "[1,1,4,2,1,1,0,0]"},
            {"input": "[30,40,50,60]", "expected": "[1,1,1,0]"},
            {"input": "[30,60,90]", "expected": "[1,1,0]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 51
    },
    {
        "title": "Evaluate Reverse Polish Notation",
        "slug": "evaluate-reverse-polish-notation",
        "difficulty": "medium",
        "category": "stacks_queues",
        "description": "You are given an array of strings tokens that represents an arithmetic expression in Reverse Polish Notation. Evaluate the expression and return an integer that represents the value of the expression. Valid operators are +, -, *, and /. Each operand may be an integer or another expression. The division between two integers always truncates toward zero.",
        "examples": [
            {"input": "tokens = [\"2\",\"1\",\"+\",\"3\",\"*\"]", "output": "9", "explanation": "((2 + 1) * 3) = 9"},
            {"input": "tokens = [\"4\",\"13\",\"5\",\"/\",\"+\"]", "output": "6", "explanation": "(4 + (13 / 5)) = 4 + 2 = 6"}
        ],
        "constraints": ["1 <= tokens.length <= 10^4", "tokens[i] is an operator or an integer in [-200, 200]"],
        "hints": ["Use a stack to evaluate the expression.", "Push numbers onto the stack. When an operator is encountered, pop two operands, apply the operator, and push the result.", "Be careful with division truncation toward zero."],
        "solution_java": """import java.util.Stack;

class Solution {
    public int evalRPN(String[] tokens) {
        Stack<Integer> stack = new Stack<>();
        for (String token : tokens) {
            switch (token) {
                case "+": stack.push(stack.pop() + stack.pop()); break;
                case "-": { int b = stack.pop(), a = stack.pop(); stack.push(a - b); break; }
                case "*": stack.push(stack.pop() * stack.pop()); break;
                case "/": { int b = stack.pop(), a = stack.pop(); stack.push(a / b); break; }
                default: stack.push(Integer.parseInt(token));
            }
        }
        return stack.pop();
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for token in tokens:
            if token in '+-*/':
                b, a = stack.pop(), stack.pop()
                if token == '+': stack.append(a + b)
                elif token == '-': stack.append(a - b)
                elif token == '*': stack.append(a * b)
                else: stack.append(int(a / b))  # truncate toward zero
            else:
                stack.append(int(token))
        return stack[0]""",
        "test_cases": [
            {"input": "[\"2\",\"1\",\"+\",\"3\",\"*\"]", "expected": "9"},
            {"input": "[\"4\",\"13\",\"5\",\"/\",\"+\"]", "expected": "6"},
            {"input": "[\"10\",\"6\",\"9\",\"3\",\"+\",\"-11\",\"*\",\"/\",\"*\",\"17\",\"+\",\"5\",\"+\"]", "expected": "22"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 52
    },
    {
        "title": "Clone Graph",
        "slug": "clone-graph",
        "difficulty": "medium",
        "category": "graphs",
        "description": "Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in the graph contains a value (int) and a list of its neighbors. The graph is represented as an adjacency list. Nodes are labeled from 1 to n.",
        "examples": [
            {"input": "adjList = [[2,4],[1,3],[2,4],[1,3]]", "output": "[[2,4],[1,3],[2,4],[1,3]]", "explanation": "4-node graph. Node 1 connects to 2,4. Node 2 connects to 1,3. Node 3 connects to 2,4. Node 4 connects to 1,3. A deep copy of the same structure is returned."},
            {"input": "adjList = [[]]", "output": "[[]]", "explanation": "Single node with no neighbors is cloned."}
        ],
        "constraints": ["0 <= number of nodes <= 100", "1 <= Node.val <= 100", "Node.val is unique for each node", "No repeated edges or self-loops"],
        "hints": ["Use a hash map to map original nodes to their clones.", "BFS or DFS from the starting node, cloning each node and its neighbors.", "Check the map before creating a clone to avoid infinite loops."],
        "solution_java": """import java.util.*;

class Solution {
    private Map<Node, Node> visited = new HashMap<>();

    public Node cloneGraph(Node node) {
        if (node == null) return null;
        if (visited.containsKey(node)) return visited.get(node);
        Node clone = new Node(node.val, new ArrayList<>());
        visited.put(node, clone);
        for (Node neighbor : node.neighbors) {
            clone.neighbors.add(cloneGraph(neighbor));
        }
        return clone;
    }
}""",
        "solution_python": """class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return None
        visited = {}

        def dfs(n):
            if n in visited:
                return visited[n]
            clone = Node(n.val, [])
            visited[n] = clone
            for neighbor in n.neighbors:
                clone.neighbors.append(dfs(neighbor))
            return clone

        return dfs(node)""",
        "test_cases": [
            {"input": "[[2,4],[1,3],[2,4],[1,3]]", "expected": "[[2,4],[1,3],[2,4],[1,3]]"},
            {"input": "[[]]", "expected": "[[]]"},
            {"input": "[]", "expected": "[]"}
        ],
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "order_index": 53
    },
    {
        "title": "Pacific Atlantic Water Flow",
        "slug": "pacific-atlantic-water-flow",
        "difficulty": "medium",
        "category": "graphs",
        "description": "There is an m x n rectangular island that borders both the Pacific Ocean and the Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges. Given an m x n integer matrix heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c), return a list of grid coordinates result where result[i] = [ri, ci] denotes that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.",
        "examples": [
            {"input": "heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]", "output": "[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]", "explanation": "These cells can reach both oceans following non-increasing paths."},
            {"input": "heights = [[1]]", "output": "[[0,0]]", "explanation": "Single cell can reach both oceans."}
        ],
        "constraints": ["m == heights.length", "n == heights[r].length", "1 <= m, n <= 200", "0 <= heights[r][c] <= 10^5"],
        "hints": ["Instead of flowing from each cell, start from the ocean borders and flow inland.", "Use two BFS/DFS passes: one from Pacific borders, one from Atlantic borders.", "The answer is cells reachable from both oceans."],
        "solution_java": """import java.util.*;

class Solution {
    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        int m = heights.length, n = heights[0].length;
        boolean[][] pacific = new boolean[m][n];
        boolean[][] atlantic = new boolean[m][n];
        for (int i = 0; i < m; i++) {
            dfs(heights, pacific, i, 0);
            dfs(heights, atlantic, i, n - 1);
        }
        for (int j = 0; j < n; j++) {
            dfs(heights, pacific, 0, j);
            dfs(heights, atlantic, m - 1, j);
        }
        List<List<Integer>> result = new ArrayList<>();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (pacific[i][j] && atlantic[i][j])
                    result.add(Arrays.asList(i, j));
        return result;
    }

    private void dfs(int[][] heights, boolean[][] visited, int i, int j) {
        if (visited[i][j]) return;
        visited[i][j] = true;
        int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
        for (int[] d : dirs) {
            int ni = i + d[0], nj = j + d[1];
            if (ni >= 0 && ni < heights.length && nj >= 0 && nj < heights[0].length
                && heights[ni][nj] >= heights[i][j])
                dfs(heights, visited, ni, nj);
        }
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights:
            return []
        m, n = len(heights), len(heights[0])

        def dfs(starts):
            visited = set(starts)
            stack = list(starts)
            while stack:
                r, c = stack.pop()
                for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited and heights[nr][nc] >= heights[r][c]:
                        visited.add((nr, nc))
                        stack.append((nr, nc))
            return visited

        pacific = dfs([(i, 0) for i in range(m)] + [(0, j) for j in range(n)])
        atlantic = dfs([(i, n-1) for i in range(m)] + [(m-1, j) for j in range(n)])
        return [[r, c] for r, c in pacific & atlantic]""",
        "test_cases": [
            {"input": "[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]", "expected": "[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]"},
            {"input": "[[1]]", "expected": "[[0,0]]"},
            {"input": "[[1,1],[1,1]]", "expected": "[[0,0],[0,1],[1,0],[1,1]]"}
        ],
        "time_complexity": "O(m * n)",
        "space_complexity": "O(m * n)",
        "order_index": 54
    },
    {
        "title": "Lowest Common Ancestor of a Binary Search Tree",
        "slug": "lowest-common-ancestor-of-bst",
        "difficulty": "medium",
        "category": "trees",
        "description": "Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes p and q in the BST. The lowest common ancestor is defined as the lowest node in T that has both p and q as descendants (where a node can be a descendant of itself).",
        "examples": [
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", "output": "6", "explanation": "The LCA of nodes 2 and 8 is 6, as 2 is in the left subtree and 8 is in the right subtree."},
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4", "output": "2", "explanation": "The LCA of nodes 2 and 4 is 2, since a node can be its own ancestor."}
        ],
        "constraints": ["2 <= number of nodes <= 10^5", "-10^9 <= Node.val <= 10^9", "All Node.val are unique", "p != q", "p and q exist in the BST"],
        "hints": ["Leverage the BST property: left subtree values < root < right subtree values.", "If both p and q are smaller than root, LCA is in the left subtree.", "If both are larger, LCA is in the right subtree. Otherwise, root is the LCA."],
        "solution_java": """class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        while (root != null) {
            if (p.val < root.val && q.val < root.val) root = root.left;
            else if (p.val > root.val && q.val > root.val) root = root.right;
            else return root;
        }
        return null;
    }
}""",
        "solution_python": """class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        while root:
            if p.val < root.val and q.val < root.val:
                root = root.left
            elif p.val > root.val and q.val > root.val:
                root = root.right
            else:
                return root""",
        "test_cases": [
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", "expected": "6"},
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4", "expected": "2"},
            {"input": "root = [2,1], p = 2, q = 1", "expected": "2"}
        ],
        "time_complexity": "O(h) where h is tree height",
        "space_complexity": "O(1)",
        "order_index": 55
    },
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "difficulty": "hard",
        "category": "arrays",
        "description": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "6 units of rain water are trapped between the bars."},
            {"input": "height = [4,2,0,3,2,5]", "output": "9", "explanation": "9 units of rain water are trapped."}
        ],
        "constraints": ["n == height.length", "1 <= n <= 2 * 10^4", "0 <= height[i] <= 10^5"],
        "hints": ["Use two pointers from both ends.", "Track the max height seen from the left and right.", "Water at each position is min(left_max, right_max) - height[i]."],
        "solution_java": """class Solution {
    public int trap(int[] height) {
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0, water = 0;
        while (left < right) {
            if (height[left] < height[right]) {
                leftMax = Math.max(leftMax, height[left]);
                water += leftMax - height[left];
                left++;
            } else {
                rightMax = Math.max(rightMax, height[right]);
                water += rightMax - height[right];
                right--;
            }
        }
        return water;
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        left_max = right_max = water = 0
        while left < right:
            if height[left] < height[right]:
                left_max = max(left_max, height[left])
                water += left_max - height[left]
                left += 1
            else:
                right_max = max(right_max, height[right])
                water += right_max - height[right]
                right -= 1
        return water""",
        "test_cases": [
            {"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expected": "6"},
            {"input": "[4,2,0,3,2,5]", "expected": "9"},
            {"input": "[1,0,1]", "expected": "1"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "order_index": 56
    },
    {
        "title": "Merge K Sorted Lists",
        "slug": "merge-k-sorted-lists",
        "difficulty": "hard",
        "category": "linked_lists",
        "description": "You are given an array of k linked-lists lists, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.",
        "examples": [
            {"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]", "explanation": "Merging [1,4,5], [1,3,4], and [2,6] produces the sorted list [1,1,2,3,4,4,5,6]."},
            {"input": "lists = []", "output": "[]", "explanation": "Empty input yields empty list."}
        ],
        "constraints": ["k == lists.length", "0 <= k <= 10^4", "0 <= lists[i].length <= 500", "-10^4 <= lists[i][j] <= 10^4", "Total nodes across all lists <= 10^4"],
        "hints": ["Use a min-heap to always pick the smallest head across all lists.", "Push the head of each non-empty list into the heap.", "After extracting the minimum, push its next node if it exists."],
        "solution_java": """import java.util.PriorityQueue;

class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
        for (ListNode node : lists)
            if (node != null) pq.offer(node);
        ListNode dummy = new ListNode(0), curr = dummy;
        while (!pq.isEmpty()) {
            ListNode min = pq.poll();
            curr.next = min;
            curr = curr.next;
            if (min.next != null) pq.offer(min.next);
        }
        return dummy.next;
    }
}""",
        "solution_python": """import heapq
from typing import List, Optional

class Solution:
    def mergeKLists(self, lists: List[Optional['ListNode']]) -> Optional['ListNode']:
        heap = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, i, node))
        dummy = curr = ListNode(0)
        while heap:
            val, i, node = heapq.heappop(heap)
            curr.next = node
            curr = curr.next
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next""",
        "test_cases": [
            {"input": "[[1,4,5],[1,3,4],[2,6]]", "expected": "[1,1,2,3,4,4,5,6]"},
            {"input": "[]", "expected": "[]"},
            {"input": "[[]]", "expected": "[]"}
        ],
        "time_complexity": "O(N log k)",
        "space_complexity": "O(k)",
        "order_index": 57
    },
    {
        "title": "Minimum Window Substring",
        "slug": "minimum-window-substring",
        "difficulty": "hard",
        "category": "strings",
        "description": "Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string. The answer is guaranteed to be unique.",
        "examples": [
            {"input": "s = \"ADOBECODEBANC\", t = \"ABC\"", "output": "\"BANC\"", "explanation": "The minimum window substring 'BANC' includes 'A', 'B', and 'C' from string t."},
            {"input": "s = \"a\", t = \"aa\"", "output": "\"\"", "explanation": "Both 'a's from t must be included in the window but s only has one 'a'."}
        ],
        "constraints": ["m == s.length, n == t.length", "1 <= m, n <= 10^5", "s and t consist of uppercase and lowercase English letters"],
        "hints": ["Use a sliding window with two pointers.", "Expand the right pointer until all characters in t are covered.", "Then contract the left pointer to minimize the window while maintaining coverage."],
        "solution_java": """import java.util.*;

class Solution {
    public String minWindow(String s, String t) {
        int[] need = new int[128], have = new int[128];
        for (char c : t.toCharArray()) need[c]++;
        int required = 0;
        for (int n : need) if (n > 0) required++;
        int formed = 0, left = 0, minLen = Integer.MAX_VALUE, minStart = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            have[c]++;
            if (need[c] > 0 && have[c] == need[c]) formed++;
            while (formed == required) {
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    minStart = left;
                }
                char lc = s.charAt(left);
                have[lc]--;
                if (need[lc] > 0 && have[lc] < need[lc]) formed--;
                left++;
            }
        }
        return minLen == Integer.MAX_VALUE ? "" : s.substring(minStart, minStart + minLen);
    }
}""",
        "solution_python": """from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)
        required = len(need)
        formed = 0
        window = {}
        left = 0
        best = (float('inf'), 0, 0)
        for right, ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1
            if ch in need and window[ch] == need[ch]:
                formed += 1
            while formed == required:
                if right - left + 1 < best[0]:
                    best = (right - left + 1, left, right)
                lc = s[left]
                window[lc] -= 1
                if lc in need and window[lc] < need[lc]:
                    formed -= 1
                left += 1
        return '' if best[0] == float('inf') else s[best[1]:best[2]+1]""",
        "test_cases": [
            {"input": "s = \"ADOBECODEBANC\", t = \"ABC\"", "expected": "\"BANC\""},
            {"input": "s = \"a\", t = \"a\"", "expected": "\"a\""},
            {"input": "s = \"a\", t = \"aa\"", "expected": "\"\""}
        ],
        "time_complexity": "O(m + n)",
        "space_complexity": "O(m + n)",
        "order_index": 58
    },
    {
        "title": "Serialize and Deserialize Binary Tree",
        "slug": "serialize-and-deserialize-binary-tree",
        "difficulty": "hard",
        "category": "trees",
        "description": "Design an algorithm to serialize and deserialize a binary tree. Serialization is the process of converting a data structure into a sequence of bits or a string so that it can be stored or transmitted and reconstructed later. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.",
        "examples": [
            {"input": "root = [1,2,3,null,null,4,5]", "output": "[1,2,3,null,null,4,5]", "explanation": "The tree is serialized and then deserialized back to its original structure."},
            {"input": "root = []", "output": "[]", "explanation": "Empty tree serializes to empty and deserializes to null."}
        ],
        "constraints": ["0 <= number of nodes <= 10^4", "-1000 <= Node.val <= 1000"],
        "hints": ["Use preorder traversal for serialization, marking null nodes with a sentinel.", "For deserialization, use a queue or iterator to reconstruct the tree recursively.", "BFS-based serialization is another valid approach."],
        "solution_java": """import java.util.*;

class Codec {
    public String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        serializeHelper(root, sb);
        return sb.toString();
    }

    private void serializeHelper(TreeNode node, StringBuilder sb) {
        if (node == null) { sb.append("null,"); return; }
        sb.append(node.val).append(",");
        serializeHelper(node.left, sb);
        serializeHelper(node.right, sb);
    }

    public TreeNode deserialize(String data) {
        Queue<String> queue = new LinkedList<>(Arrays.asList(data.split(",")));
        return deserializeHelper(queue);
    }

    private TreeNode deserializeHelper(Queue<String> queue) {
        String val = queue.poll();
        if ("null".equals(val)) return null;
        TreeNode node = new TreeNode(Integer.parseInt(val));
        node.left = deserializeHelper(queue);
        node.right = deserializeHelper(queue);
        return node;
    }
}""",
        "solution_python": """class Codec:
    def serialize(self, root):
        vals = []
        def preorder(node):
            if not node:
                vals.append('null')
                return
            vals.append(str(node.val))
            preorder(node.left)
            preorder(node.right)
        preorder(root)
        return ','.join(vals)

    def deserialize(self, data):
        vals = iter(data.split(','))
        def build():
            val = next(vals)
            if val == 'null':
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        return build()""",
        "test_cases": [
            {"input": "[1,2,3,null,null,4,5]", "expected": "[1,2,3,null,null,4,5]"},
            {"input": "[]", "expected": "[]"},
            {"input": "[1]", "expected": "[1]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 59
    },
    {
        "title": "Word Ladder",
        "slug": "word-ladder",
        "difficulty": "hard",
        "category": "graphs",
        "description": "A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence beginWord -> s1 -> s2 -> ... -> sk such that every adjacent pair of words differs by a single letter, every si is in wordList, and sk == endWord. Given beginWord, endWord, and wordList, return the number of words in the shortest transformation sequence, or 0 if no such sequence exists.",
        "examples": [
            {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]", "output": "5", "explanation": "hit -> hot -> dot -> dog -> cog is the shortest path with length 5."},
            {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]", "output": "0", "explanation": "endWord 'cog' is not in wordList, so no valid transformation exists."}
        ],
        "constraints": ["1 <= beginWord.length <= 10", "endWord.length == beginWord.length", "1 <= wordList.length <= 5000", "All words have the same length", "Words consist of lowercase English letters", "All words in wordList are unique"],
        "hints": ["Use BFS, treating each word as a node and one-letter differences as edges.", "For each word, generate all possible one-letter transformations and check if they exist in the wordList.", "Use a set for O(1) word lookup."],
        "solution_java": """import java.util.*;

class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> wordSet = new HashSet<>(wordList);
        if (!wordSet.contains(endWord)) return 0;
        Queue<String> queue = new LinkedList<>();
        queue.offer(beginWord);
        int level = 1;
        while (!queue.isEmpty()) {
            int size = queue.size();
            for (int i = 0; i < size; i++) {
                char[] word = queue.poll().toCharArray();
                for (int j = 0; j < word.length; j++) {
                    char orig = word[j];
                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == orig) continue;
                        word[j] = c;
                        String next = new String(word);
                        if (next.equals(endWord)) return level + 1;
                        if (wordSet.remove(next)) queue.offer(next);
                    }
                    word[j] = orig;
                }
            }
            level++;
        }
        return 0;
    }
}""",
        "solution_python": """from collections import deque
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0
        queue = deque([(beginWord, 1)])
        while queue:
            word, level = queue.popleft()
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i+1:]
                    if next_word == endWord:
                        return level + 1
                    if next_word in word_set:
                        word_set.remove(next_word)
                        queue.append((next_word, level + 1))
        return 0""",
        "test_cases": [
            {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]", "expected": "5"},
            {"input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]", "expected": "0"},
            {"input": "beginWord = \"a\", endWord = \"c\", wordList = [\"a\",\"b\",\"c\"]", "expected": "2"}
        ],
        "time_complexity": "O(m^2 * n)",
        "space_complexity": "O(m * n)",
        "order_index": 60
    },
    {
        "title": "Longest Valid Parentheses",
        "slug": "longest-valid-parentheses",
        "difficulty": "hard",
        "category": "dynamic_programming",
        "description": "Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring.",
        "examples": [
            {"input": "s = \"(()\"", "output": "2", "explanation": "The longest valid parentheses substring is '()'."},
            {"input": "s = \")()())\"", "output": "4", "explanation": "The longest valid parentheses substring is '()()', which has length 4."}
        ],
        "constraints": ["0 <= s.length <= 3 * 10^4", "s[i] is '(' or ')'"],
        "hints": ["Use a stack to track indices of unmatched parentheses.", "Push index of '(' onto the stack. For ')', pop and calculate length if stack is not empty.", "Keep a base index on the stack for computing lengths."],
        "solution_java": """import java.util.Stack;

class Solution {
    public int longestValidParentheses(String s) {
        Stack<Integer> stack = new Stack<>();
        stack.push(-1);
        int maxLen = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                stack.push(i);
            } else {
                stack.pop();
                if (stack.isEmpty()) {
                    stack.push(i);
                } else {
                    maxLen = Math.max(maxLen, i - stack.peek());
                }
            }
        }
        return maxLen;
    }
}""",
        "solution_python": """class Solution:
    def longestValidParentheses(self, s: str) -> int:
        stack = [-1]
        max_len = 0
        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    max_len = max(max_len, i - stack[-1])
        return max_len""",
        "test_cases": [
            {"input": "\"(()\"", "expected": "2"},
            {"input": "\")()())\"", "expected": "4"},
            {"input": "\"\"", "expected": "0"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 61
    },
    {
        "title": "Edit Distance",
        "slug": "edit-distance",
        "difficulty": "hard",
        "category": "dynamic_programming",
        "description": "Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2. You have three operations permitted: insert a character, delete a character, or replace a character.",
        "examples": [
            {"input": "word1 = \"horse\", word2 = \"ros\"", "output": "3", "explanation": "horse -> rorse (replace 'h' with 'r') -> rose (remove 'r') -> ros (remove 'e')."},
            {"input": "word1 = \"intention\", word2 = \"execution\"", "output": "5", "explanation": "intention -> inention -> enention -> exention -> exection -> execution."}
        ],
        "constraints": ["0 <= word1.length, word2.length <= 500", "word1 and word2 consist of lowercase English letters"],
        "hints": ["Use 2D DP where dp[i][j] is the edit distance between word1[0..i-1] and word2[0..j-1].", "If characters match, dp[i][j] = dp[i-1][j-1].", "Otherwise, dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) for delete, insert, replace."],
        "solution_java": """class Solution {
    public int minDistance(String word1, String word2) {
        int m = word1.length(), n = word2.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(dp[i - 1][j - 1],
                                   Math.min(dp[i - 1][j], dp[i][j - 1]));
                }
            }
        }
        return dp[m][n];
    }
}""",
        "solution_python": """class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
        return dp[m][n]""",
        "test_cases": [
            {"input": "word1 = \"horse\", word2 = \"ros\"", "expected": "3"},
            {"input": "word1 = \"intention\", word2 = \"execution\"", "expected": "5"},
            {"input": "word1 = \"\", word2 = \"a\"", "expected": "1"}
        ],
        "time_complexity": "O(m * n)",
        "space_complexity": "O(m * n)",
        "order_index": 62
    },
    {
        "title": "Regular Expression Matching",
        "slug": "regular-expression-matching",
        "difficulty": "hard",
        "category": "dynamic_programming",
        "description": "Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where '.' matches any single character and '*' matches zero or more of the preceding element. The matching should cover the entire input string (not partial).",
        "examples": [
            {"input": "s = \"aa\", p = \"a\"", "output": "false", "explanation": "'a' does not match the entire string 'aa'."},
            {"input": "s = \"aa\", p = \"a*\"", "output": "true", "explanation": "'*' means zero or more of the preceding element 'a'. Therefore, by repeating 'a' once, it becomes 'aa'."}
        ],
        "constraints": ["1 <= s.length <= 20", "1 <= p.length <= 20", "s contains only lowercase English letters", "p contains only lowercase English letters, '.', and '*'"],
        "hints": ["Use 2D DP where dp[i][j] means s[0..i-1] matches p[0..j-1].", "Handle '*' by considering zero occurrences (dp[i][j-2]) or one+ occurrences.", "For '.', it matches any character so treat it like a match."],
        "solution_java": """class Solution {
    public boolean isMatch(String s, String p) {
        int m = s.length(), n = p.length();
        boolean[][] dp = new boolean[m + 1][n + 1];
        dp[0][0] = true;
        for (int j = 1; j <= n; j++) {
            if (p.charAt(j - 1) == '*') dp[0][j] = dp[0][j - 2];
        }
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (p.charAt(j - 1) == '*') {
                    dp[i][j] = dp[i][j - 2]; // zero occurrences
                    if (p.charAt(j - 2) == '.' || p.charAt(j - 2) == s.charAt(i - 1))
                        dp[i][j] |= dp[i - 1][j]; // one or more
                } else if (p.charAt(j - 1) == '.' || p.charAt(j - 1) == s.charAt(i - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                }
            }
        }
        return dp[m][n];
    }
}""",
        "solution_python": """class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[0][j] = dp[0][j-2]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j-1] == '*':
                    dp[i][j] = dp[i][j-2]  # zero occurrences
                    if p[j-2] == '.' or p[j-2] == s[i-1]:
                        dp[i][j] = dp[i][j] or dp[i-1][j]
                elif p[j-1] == '.' or p[j-1] == s[i-1]:
                    dp[i][j] = dp[i-1][j-1]
        return dp[m][n]""",
        "test_cases": [
            {"input": "s = \"aa\", p = \"a\"", "expected": "false"},
            {"input": "s = \"aa\", p = \"a*\"", "expected": "true"},
            {"input": "s = \"ab\", p = \".*\"", "expected": "true"}
        ],
        "time_complexity": "O(m * n)",
        "space_complexity": "O(m * n)",
        "order_index": 63
    },
    {
        "title": "Median of Two Sorted Arrays",
        "slug": "median-of-two-sorted-arrays",
        "difficulty": "hard",
        "category": "sorting_searching",
        "description": "Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays. The overall run time complexity should be O(log(min(m,n))).",
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.0", "explanation": "Merged array = [1,2,3]. Median is 2.0."},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.5", "explanation": "Merged array = [1,2,3,4]. Median is (2+3)/2 = 2.5."}
        ],
        "constraints": ["nums1.length == m, nums2.length == n", "0 <= m <= 1000, 0 <= n <= 1000", "1 <= m + n <= 2000", "-10^6 <= nums1[i], nums2[i] <= 10^6"],
        "hints": ["Binary search on the shorter array to find the correct partition.", "Partition both arrays such that elements on the left are all smaller than elements on the right.", "The median comes from the max of the left partition and min of the right partition."],
        "solution_java": """class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        if (nums1.length > nums2.length) return findMedianSortedArrays(nums2, nums1);
        int m = nums1.length, n = nums2.length;
        int lo = 0, hi = m;
        while (lo <= hi) {
            int i = (lo + hi) / 2;
            int j = (m + n + 1) / 2 - i;
            int maxLeft1 = (i == 0) ? Integer.MIN_VALUE : nums1[i - 1];
            int minRight1 = (i == m) ? Integer.MAX_VALUE : nums1[i];
            int maxLeft2 = (j == 0) ? Integer.MIN_VALUE : nums2[j - 1];
            int minRight2 = (j == n) ? Integer.MAX_VALUE : nums2[j];
            if (maxLeft1 <= minRight2 && maxLeft2 <= minRight1) {
                if ((m + n) % 2 == 0)
                    return (Math.max(maxLeft1, maxLeft2) + Math.min(minRight1, minRight2)) / 2.0;
                return Math.max(maxLeft1, maxLeft2);
            } else if (maxLeft1 > minRight2) hi = i - 1;
            else lo = i + 1;
        }
        return 0.0;
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        lo, hi = 0, m
        while lo <= hi:
            i = (lo + hi) // 2
            j = (m + n + 1) // 2 - i
            max_left1 = float('-inf') if i == 0 else nums1[i-1]
            min_right1 = float('inf') if i == m else nums1[i]
            max_left2 = float('-inf') if j == 0 else nums2[j-1]
            min_right2 = float('inf') if j == n else nums2[j]
            if max_left1 <= min_right2 and max_left2 <= min_right1:
                if (m + n) % 2 == 0:
                    return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
                return float(max(max_left1, max_left2))
            elif max_left1 > min_right2:
                hi = i - 1
            else:
                lo = i + 1
        return 0.0""",
        "test_cases": [
            {"input": "nums1 = [1,3], nums2 = [2]", "expected": "2.0"},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "expected": "2.5"},
            {"input": "nums1 = [0,0], nums2 = [0,0]", "expected": "0.0"}
        ],
        "time_complexity": "O(log(min(m, n)))",
        "space_complexity": "O(1)",
        "order_index": 64
    },
    {
        "title": "Sliding Window Maximum",
        "slug": "sliding-window-maximum",
        "difficulty": "hard",
        "category": "stacks_queues",
        "description": "You are given an array of integers nums and there is a sliding window of size k which moves from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position, return the max value in the window.",
        "examples": [
            {"input": "nums = [1,3,-1,-3,5,3,6,7], k = 3", "output": "[3,3,5,5,6,7]", "explanation": "Window positions: [1,3,-1] max=3; [3,-1,-3] max=3; [-1,-3,5] max=5; [-3,5,3] max=5; [5,3,6] max=6; [3,6,7] max=7."},
            {"input": "nums = [1], k = 1", "output": "[1]", "explanation": "Single element, single window."}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "1 <= k <= nums.length"],
        "hints": ["Use a monotonic deque that stores indices in decreasing order of their values.", "Remove indices from the front if they are outside the window.", "Remove indices from the back if the current value is greater (they can never be the max)."],
        "solution_java": """import java.util.*;

class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length;
        int[] result = new int[n - k + 1];
        Deque<Integer> deque = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!deque.isEmpty() && deque.peekFirst() < i - k + 1) deque.pollFirst();
            while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) deque.pollLast();
            deque.offerLast(i);
            if (i >= k - 1) result[i - k + 1] = nums[deque.peekFirst()];
        }
        return result;
    }
}""",
        "solution_python": """from collections import deque
from typing import List

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        dq = deque()
        result = []
        for i in range(len(nums)):
            while dq and dq[0] < i - k + 1:
                dq.popleft()
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()
            dq.append(i)
            if i >= k - 1:
                result.append(nums[dq[0]])
        return result""",
        "test_cases": [
            {"input": "nums = [1,3,-1,-3,5,3,6,7], k = 3", "expected": "[3,3,5,5,6,7]"},
            {"input": "nums = [1], k = 1", "expected": "[1]"},
            {"input": "nums = [1,-1], k = 1", "expected": "[1,-1]"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(k)",
        "order_index": 65
    },
    {
        "title": "Alien Dictionary",
        "slug": "alien-dictionary",
        "difficulty": "hard",
        "category": "graphs",
        "description": "There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you. You are given a list of strings words from the alien language's dictionary, where the strings are sorted lexicographically by the rules of this new language. Derive the order of letters in this language. If the order is invalid, return an empty string. If there are multiple valid orderings, return any of them.",
        "examples": [
            {"input": "words = [\"wrt\",\"wrf\",\"er\",\"ett\",\"rftt\"]", "output": "\"wertf\"", "explanation": "From the given words we can derive: 't' comes before 'f' (wrt vs wrf), 'w' before 'e' (wrt vs er), 'r' before 't' (er vs ett), 'e' before 'r' (ett vs rftt)."},
            {"input": "words = [\"z\",\"x\"]", "output": "\"zx\"", "explanation": "From the dictionary order, 'z' comes before 'x'."}
        ],
        "constraints": ["1 <= words.length <= 100", "1 <= words[i].length <= 100", "words[i] consists of only lowercase English letters"],
        "hints": ["Build a directed graph from adjacent word pairs by comparing character by character.", "The first differing character gives an edge in the graph.", "Use topological sort (BFS with in-degree or DFS) to find the ordering."],
        "solution_java": """import java.util.*;

class Solution {
    public String alienOrder(String[] words) {
        Map<Character, Set<Character>> graph = new HashMap<>();
        Map<Character, Integer> inDegree = new HashMap<>();
        for (String w : words)
            for (char c : w.toCharArray()) {
                graph.putIfAbsent(c, new HashSet<>());
                inDegree.putIfAbsent(c, 0);
            }
        for (int i = 0; i < words.length - 1; i++) {
            String w1 = words[i], w2 = words[i + 1];
            if (w1.length() > w2.length() && w1.startsWith(w2)) return "";
            for (int j = 0; j < Math.min(w1.length(), w2.length()); j++) {
                char c1 = w1.charAt(j), c2 = w2.charAt(j);
                if (c1 != c2) {
                    if (graph.get(c1).add(c2))
                        inDegree.merge(c2, 1, Integer::sum);
                    break;
                }
            }
        }
        Queue<Character> queue = new LinkedList<>();
        for (var e : inDegree.entrySet())
            if (e.getValue() == 0) queue.offer(e.getKey());
        StringBuilder sb = new StringBuilder();
        while (!queue.isEmpty()) {
            char c = queue.poll();
            sb.append(c);
            for (char next : graph.get(c)) {
                inDegree.merge(next, -1, Integer::sum);
                if (inDegree.get(next) == 0) queue.offer(next);
            }
        }
        return sb.length() == inDegree.size() ? sb.toString() : "";
    }
}""",
        "solution_python": """from collections import defaultdict, deque
from typing import List

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        graph = defaultdict(set)
        in_degree = {c: 0 for w in words for c in w}
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i+1]
            if len(w1) > len(w2) and w1.startswith(w2):
                return ''
            for c1, c2 in zip(w1, w2):
                if c1 != c2:
                    if c2 not in graph[c1]:
                        graph[c1].add(c2)
                        in_degree[c2] += 1
                    break
        queue = deque(c for c in in_degree if in_degree[c] == 0)
        result = []
        while queue:
            c = queue.popleft()
            result.append(c)
            for nxt in graph[c]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)
        return ''.join(result) if len(result) == len(in_degree) else ''""",
        "test_cases": [
            {"input": "[\"wrt\",\"wrf\",\"er\",\"ett\",\"rftt\"]", "expected": "\"wertf\""},
            {"input": "[\"z\",\"x\"]", "expected": "\"zx\""},
            {"input": "[\"z\",\"x\",\"z\"]", "expected": "\"\""}
        ],
        "time_complexity": "O(C) where C is total chars across all words",
        "space_complexity": "O(1) (26 letters max)",
        "order_index": 66
    },
    {
        "title": "N-Queens",
        "slug": "n-queens",
        "difficulty": "hard",
        "category": "backtracking",
        "description": "The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other. Given an integer n, return all distinct solutions to the n-queens puzzle. Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' indicates a queen and '.' indicates an empty space.",
        "examples": [
            {"input": "n = 4", "output": "[[\".Q..\",\"...Q\",\"Q...\",\"..Q.\"],[\"..Q.\",\"Q...\",\"...Q\",\".Q..\"]]", "explanation": "There are two distinct solutions to the 4-queens puzzle."},
            {"input": "n = 1", "output": "[[\"Q\"]]", "explanation": "Single queen on a 1x1 board."}
        ],
        "constraints": ["1 <= n <= 9"],
        "hints": ["Place queens row by row using backtracking.", "Track which columns, diagonals, and anti-diagonals are under attack.", "A diagonal is identified by row-col, an anti-diagonal by row+col."],
        "solution_java": """import java.util.*;

class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> result = new ArrayList<>();
        backtrack(n, 0, new int[n], new boolean[n], new boolean[2*n], new boolean[2*n], result);
        return result;
    }

    private void backtrack(int n, int row, int[] queens, boolean[] cols,
                           boolean[] diag, boolean[] antiDiag, List<List<String>> result) {
        if (row == n) {
            List<String> board = new ArrayList<>();
            for (int r = 0; r < n; r++) {
                char[] line = new char[n];
                Arrays.fill(line, '.');
                line[queens[r]] = 'Q';
                board.add(new String(line));
            }
            result.add(board);
            return;
        }
        for (int col = 0; col < n; col++) {
            if (cols[col] || diag[row - col + n] || antiDiag[row + col]) continue;
            queens[row] = col;
            cols[col] = diag[row - col + n] = antiDiag[row + col] = true;
            backtrack(n, row + 1, queens, cols, diag, antiDiag, result);
            cols[col] = diag[row - col + n] = antiDiag[row + col] = false;
        }
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []
        cols = set()
        diag = set()
        anti = set()
        board = [['.' ] * n for _ in range(n)]

        def backtrack(row):
            if row == n:
                result.append([''.join(r) for r in board])
                return
            for col in range(n):
                if col in cols or (row - col) in diag or (row + col) in anti:
                    continue
                cols.add(col)
                diag.add(row - col)
                anti.add(row + col)
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'
                cols.discard(col)
                diag.discard(row - col)
                anti.discard(row + col)

        backtrack(0)
        return result""",
        "test_cases": [
            {"input": "4", "expected": "[[\".Q..\",\"...Q\",\"Q...\",\"..Q.\"],[\"..Q.\",\"Q...\",\"...Q\",\".Q..\"]]"},
            {"input": "1", "expected": "[[\"Q\"]]"},
            {"input": "2", "expected": "[]"}
        ],
        "time_complexity": "O(n!)",
        "space_complexity": "O(n^2)",
        "order_index": 67
    },
    {
        "title": "Longest Consecutive Sequence",
        "slug": "longest-consecutive-sequence",
        "difficulty": "hard",
        "category": "hash_maps",
        "description": "Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence. You must write an algorithm that runs in O(n) time.",
        "examples": [
            {"input": "nums = [100,4,200,1,3,2]", "output": "4", "explanation": "The longest consecutive sequence is [1,2,3,4], length 4."},
            {"input": "nums = [0,3,7,2,5,8,4,6,0,1]", "output": "9", "explanation": "The longest consecutive sequence is [0,1,2,3,4,5,6,7,8], length 9."}
        ],
        "constraints": ["0 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "hints": ["Put all numbers in a hash set for O(1) lookup.", "Only start counting from numbers that are the beginning of a sequence (num-1 not in the set).", "Extend the sequence forward and track the maximum length."],
        "solution_java": """import java.util.*;

class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int n : nums) set.add(n);
        int longest = 0;
        for (int n : set) {
            if (!set.contains(n - 1)) {
                int len = 1;
                while (set.contains(n + len)) len++;
                longest = Math.max(longest, len);
            }
        }
        return longest;
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0
        for n in num_set:
            if n - 1 not in num_set:
                length = 1
                while n + length in num_set:
                    length += 1
                longest = max(longest, length)
        return longest""",
        "test_cases": [
            {"input": "[100,4,200,1,3,2]", "expected": "4"},
            {"input": "[0,3,7,2,5,8,4,6,0,1]", "expected": "9"},
            {"input": "[]", "expected": "0"}
        ],
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "order_index": 68
    },
    {
        "title": "Word Search II",
        "slug": "word-search-ii",
        "difficulty": "hard",
        "category": "backtracking",
        "description": "Given an m x n board of characters and a list of strings words, return all words on the board. Each word must be constructed from letters of sequentially adjacent cells (horizontally or vertically neighboring). The same letter cell may not be used more than once in a word.",
        "examples": [
            {"input": "board = [[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], words = [\"oath\",\"pea\",\"eat\",\"rain\"]", "output": "[\"eat\",\"oath\"]", "explanation": "Both 'eat' and 'oath' can be found on the board."},
            {"input": "board = [[\"a\",\"b\"],[\"c\",\"d\"]], words = [\"abcb\"]", "output": "[]", "explanation": "'abcb' cannot be formed without reusing cells."}
        ],
        "constraints": ["m == board.length, n == board[i].length", "1 <= m, n <= 12", "1 <= words.length <= 3 * 10^4", "1 <= words[i].length <= 10"],
        "hints": ["Build a trie from the word list for efficient prefix matching.", "DFS from each cell, following trie nodes.", "Remove found words from the trie to avoid duplicates and prune empty branches."],
        "solution_java": """import java.util.*;

class Solution {
    class TrieNode {
        TrieNode[] children = new TrieNode[26];
        String word = null;
    }

    public List<String> findWords(char[][] board, String[] words) {
        TrieNode root = new TrieNode();
        for (String w : words) {
            TrieNode node = root;
            for (char c : w.toCharArray()) {
                int idx = c - 'a';
                if (node.children[idx] == null) node.children[idx] = new TrieNode();
                node = node.children[idx];
            }
            node.word = w;
        }
        List<String> result = new ArrayList<>();
        for (int i = 0; i < board.length; i++)
            for (int j = 0; j < board[0].length; j++)
                dfs(board, i, j, root, result);
        return result;
    }

    private void dfs(char[][] board, int i, int j, TrieNode node, List<String> result) {
        if (i < 0 || i >= board.length || j < 0 || j >= board[0].length) return;
        char c = board[i][j];
        if (c == '#' || node.children[c - 'a'] == null) return;
        node = node.children[c - 'a'];
        if (node.word != null) { result.add(node.word); node.word = null; }
        board[i][j] = '#';
        dfs(board, i+1, j, node, result);
        dfs(board, i-1, j, node, result);
        dfs(board, i, j+1, node, result);
        dfs(board, i, j-1, node, result);
        board[i][j] = c;
    }
}""",
        "solution_python": """from typing import List

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = {}
        for word in words:
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            node['$'] = word

        m, n = len(board), len(board[0])
        result = []

        def dfs(i, j, node):
            if i < 0 or i >= m or j < 0 or j >= n:
                return
            ch = board[i][j]
            if ch not in node:
                return
            child = node[ch]
            if '$' in child:
                result.append(child.pop('$'))
            board[i][j] = '#'
            for di, dj in [(1,0),(-1,0),(0,1),(0,-1)]:
                dfs(i+di, j+dj, child)
            board[i][j] = ch
            if not child:
                del node[ch]

        for i in range(m):
            for j in range(n):
                dfs(i, j, root)
        return result""",
        "test_cases": [
            {"input": "board = [[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], words = [\"oath\",\"pea\",\"eat\",\"rain\"]", "expected": "[\"eat\",\"oath\"]"},
            {"input": "board = [[\"a\",\"b\"],[\"c\",\"d\"]], words = [\"abcb\"]", "expected": "[]"},
            {"input": "board = [[\"a\"]], words = [\"a\"]", "expected": "[\"a\"]"}
        ],
        "time_complexity": "O(m * n * 4^L)",
        "space_complexity": "O(sum of word lengths)",
        "order_index": 69
    },
    {
        "title": "Find Median from Data Stream",
        "slug": "find-median-from-data-stream",
        "difficulty": "hard",
        "category": "sorting_searching",
        "description": "The median is the middle value in an ordered integer list. If the size of the list is even, the median is the mean of the two middle values. Implement the MedianFinder class: MedianFinder() initializes the object, addNum(int num) adds the integer num to the data structure, and findMedian() returns the median of all elements so far.",
        "examples": [
            {"input": "[\"MedianFinder\",\"addNum\",\"addNum\",\"findMedian\",\"addNum\",\"findMedian\"]\n[[],[1],[2],[],[3],[]]", "output": "[null,null,null,1.5,null,2.0]", "explanation": "After adding 1 and 2, median is (1+2)/2 = 1.5. After adding 3, median is 2.0."},
            {"input": "[\"MedianFinder\",\"addNum\",\"findMedian\"]\n[[],[5],[]]", "output": "[null,null,5.0]", "explanation": "Single element, median is 5.0."}
        ],
        "constraints": ["-10^5 <= num <= 10^5", "There will be at least one element before findMedian is called", "At most 5 * 10^4 calls to addNum and findMedian"],
        "hints": ["Use two heaps: a max-heap for the lower half and a min-heap for the upper half.", "Keep the heaps balanced so that the max-heap has at most one extra element.", "The median is either the top of the max-heap or the average of both tops."],
        "solution_java": """import java.util.*;

class MedianFinder {
    private PriorityQueue<Integer> lo = new PriorityQueue<>(Collections.reverseOrder()); // max-heap
    private PriorityQueue<Integer> hi = new PriorityQueue<>(); // min-heap

    public MedianFinder() {}

    public void addNum(int num) {
        lo.offer(num);
        hi.offer(lo.poll());
        if (lo.size() < hi.size()) lo.offer(hi.poll());
    }

    public double findMedian() {
        if (lo.size() > hi.size()) return lo.peek();
        return (lo.peek() + hi.peek()) / 2.0;
    }
}""",
        "solution_python": """import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negated)
        self.hi = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0""",
        "test_cases": [
            {"input": "[[],[1],[2],[],[3],[]]", "expected": "[null,null,null,1.5,null,2.0]"},
            {"input": "[[],[5],[]]", "expected": "[null,null,5.0]"},
            {"input": "[[],[1],[],[2],[],[3],[]]", "expected": "[null,null,1.0,null,1.5,null,2.0]"}
        ],
        "time_complexity": "O(log n) per addNum, O(1) per findMedian",
        "space_complexity": "O(n)",
        "order_index": 70
    },
]


# ======================================================================
# STAR QUESTIONS DATA
# ======================================================================

STAR_QUESTIONS = [
    # ── Leadership (7) ──
    {
        "category": "leadership",
        "question": "Tell me about a time you had to drive technical alignment across multiple teams with conflicting priorities.",
        "tips": [
            "Describe the specific mechanism you used to build consensus, such as an RFC, a design review, or a series of one-on-ones with tech leads.",
            "Quantify the impact of alignment - faster delivery, fewer integration bugs, or reduced duplicate work.",
            "Show that you balanced technical correctness with organizational pragmatism rather than forcing a single answer."
        ],
        "order_index": 1
    },
    {
        "category": "leadership",
        "question": "Describe a situation where you defined and drove a multi-quarter technical roadmap for your team or organization.",
        "tips": [
            "Explain how you gathered input from stakeholders, product managers, and engineers to shape the roadmap.",
            "Highlight how you sequenced work to deliver incremental value while building toward the larger vision.",
            "Mention how you handled changes or pivots to the roadmap when business priorities shifted."
        ],
        "order_index": 2
    },
    {
        "category": "leadership",
        "question": "Tell me about a time you had to make an unpopular technical decision and bring the team along.",
        "tips": [
            "Focus on the data and reasoning you presented to justify the decision rather than relying on authority.",
            "Acknowledge the concerns people had and describe how you addressed them directly.",
            "Share the outcome and whether the team eventually agreed the decision was right."
        ],
        "order_index": 3
    },
    {
        "category": "leadership",
        "question": "Describe how you established or improved engineering standards and practices across your organization.",
        "tips": [
            "Be specific about which standards you introduced - code review guidelines, testing requirements, deployment checklists, or architectural principles.",
            "Explain how you got buy-in from other senior engineers rather than mandating changes top-down.",
            "Share measurable improvements such as reduced incident rates, faster onboarding, or fewer production regressions."
        ],
        "order_index": 4
    },
    {
        "category": "leadership",
        "question": "Tell me about a time you identified a critical technical risk that others had overlooked and led the effort to mitigate it.",
        "tips": [
            "Explain what made the risk non-obvious and how you discovered it through analysis, monitoring, or experience.",
            "Describe how you communicated the urgency to leadership and secured resources to address it.",
            "Quantify the potential impact if the risk had materialized versus the cost of mitigation."
        ],
        "order_index": 5
    },
    {
        "category": "leadership",
        "question": "Describe a situation where you had to lead a large-scale system migration or re-architecture effort.",
        "tips": [
            "Explain the migration strategy - big bang versus incremental, strangler fig pattern, or parallel running - and why you chose it.",
            "Highlight how you managed risk with rollback plans, feature flags, and staged rollouts.",
            "Discuss how you kept the team motivated during the long migration while still delivering product features."
        ],
        "order_index": 6
    },
    {
        "category": "leadership",
        "question": "Tell me about a time you mentored a junior or mid-level engineer who went on to significantly grow in their career.",
        "tips": [
            "Describe specific actions you took - pairing sessions, stretch assignments, feedback conversations - not just general availability.",
            "Show how you adapted your mentoring style to the individual's needs and learning pace.",
            "Share the concrete career outcome for the mentee, such as a promotion, leading a project, or becoming a domain expert."
        ],
        "order_index": 7
    },

    # ── Conflict (6) ──
    {
        "category": "conflict",
        "question": "Tell me about a time you had a significant technical disagreement with another senior engineer or architect.",
        "tips": [
            "Show that you engaged with the other person's position seriously and understood their reasoning before presenting your own.",
            "Describe how you moved the discussion from opinions to evidence - prototypes, benchmarks, or production data.",
            "Explain the resolution and whether you compromised, deferred to their judgment, or found a third option."
        ],
        "order_index": 8
    },
    {
        "category": "conflict",
        "question": "Describe a situation where two teams you worked with had conflicting technical approaches and you had to mediate.",
        "tips": [
            "Explain the root cause of the conflict - different constraints, assumptions, or priorities - not just the surface disagreement.",
            "Describe the process you used to bring both sides together, such as a joint design session or shared success criteria.",
            "Show that the resolution strengthened the working relationship rather than leaving one side feeling overruled."
        ],
        "order_index": 9
    },
    {
        "category": "conflict",
        "question": "Tell me about a time you pushed back on a product requirement because of technical concerns.",
        "tips": [
            "Frame the pushback as advocating for the user or the business, not just engineering preferences.",
            "Describe the alternative you proposed and how it addressed the product need with acceptable trade-offs.",
            "Mention whether you were successful and what you learned about communicating technical constraints to non-technical stakeholders."
        ],
        "order_index": 10
    },
    {
        "category": "conflict",
        "question": "Describe a time when you had to address underperformance or problematic behavior in a peer or direct report.",
        "tips": [
            "Explain how you approached the conversation with empathy and specific examples rather than vague criticism.",
            "Describe the support or structure you put in place to help the person improve.",
            "Share the outcome honestly, whether it was a turnaround, a role change, or a departure."
        ],
        "order_index": 11
    },
    {
        "category": "conflict",
        "question": "Tell me about a time you disagreed with your manager or skip-level on a technical direction.",
        "tips": [
            "Show that you escalated the disagreement constructively with data and alternatives, not just complaints.",
            "Describe how you managed the relationship through the disagreement without undermining trust.",
            "Explain the outcome and what you learned about influencing without authority."
        ],
        "order_index": 12
    },
    {
        "category": "conflict",
        "question": "Describe a situation where competing priorities between your team and another team created tension during a critical project.",
        "tips": [
            "Explain the business context that made both teams' priorities legitimate.",
            "Describe how you found a path forward - shared resources, re-sequencing, or escalation to aligned leadership.",
            "Highlight any lasting changes to processes or communication patterns that prevented future conflicts."
        ],
        "order_index": 13
    },

    # ── Failure (6) ──
    {
        "category": "failure",
        "question": "Tell me about a production incident you caused or contributed to and how you handled it.",
        "tips": [
            "Be honest about your role in the incident without deflecting blame to tools or other people.",
            "Focus on the investigation and resolution process, especially how you coordinated with others under pressure.",
            "Describe the systemic improvements you drove afterward - better testing, monitoring, deployment guards, or runbooks."
        ],
        "order_index": 14
    },
    {
        "category": "failure",
        "question": "Describe a project you led that failed to meet its goals. What did you learn?",
        "tips": [
            "Be specific about what failed - missed deadline, wrong technical approach, poor adoption - rather than being vague.",
            "Show that you took ownership and conducted an honest retrospective rather than looking for external excuses.",
            "Explain the concrete changes you made to your approach in subsequent projects as a result."
        ],
        "order_index": 15
    },
    {
        "category": "failure",
        "question": "Tell me about a time you made an architectural decision that turned out to be wrong.",
        "tips": [
            "Explain the reasoning that led to the decision and why it seemed sound at the time.",
            "Describe how you recognized the mistake - through metrics, feedback, or hands-on experience.",
            "Show how you course-corrected, including how you communicated the change to stakeholders who had invested in the original direction."
        ],
        "order_index": 16
    },
    {
        "category": "failure",
        "question": "Describe a time you underestimated the complexity of a technical problem and it impacted delivery.",
        "tips": [
            "Explain the specific complexities you missed - integration challenges, data migration edge cases, or performance at scale.",
            "Describe how you communicated the delay and re-planned with stakeholders.",
            "Share what estimation or discovery techniques you adopted afterward to avoid similar surprises."
        ],
        "order_index": 17
    },
    {
        "category": "failure",
        "question": "Tell me about a time your team shipped a feature that did not deliver the expected business impact.",
        "tips": [
            "Show that you measured the impact rather than assuming success after launch.",
            "Describe the analysis you did to understand why the feature underperformed.",
            "Explain the decision you made - iterate, pivot, or deprecate - and how you justified it to leadership."
        ],
        "order_index": 18
    },
    {
        "category": "failure",
        "question": "Describe a hiring decision you made or influenced that did not work out.",
        "tips": [
            "Reflect on what signals you missed during the interview process or what biases influenced the decision.",
            "Describe how you handled the situation fairly for the person involved.",
            "Explain what you changed about your evaluation criteria or interview process going forward."
        ],
        "order_index": 19
    },

    # ── Innovation (6) ──
    {
        "category": "innovation",
        "question": "Tell me about a time you introduced a new technology or tool that significantly improved your team's productivity.",
        "tips": [
            "Explain the evaluation process - how you assessed alternatives and validated the choice with a proof of concept.",
            "Describe how you managed the adoption curve, including training, documentation, and early wins.",
            "Quantify the productivity improvement with specific metrics like build times, deployment frequency, or developer satisfaction."
        ],
        "order_index": 20
    },
    {
        "category": "innovation",
        "question": "Describe a time you identified an opportunity to automate a manual process that was consuming significant engineering time.",
        "tips": [
            "Explain how you quantified the time being wasted to build a business case for the automation work.",
            "Describe the solution you built and the trade-offs you made between perfect automation and pragmatic improvement.",
            "Share the time savings and any unexpected benefits like reduced errors or improved consistency."
        ],
        "order_index": 21
    },
    {
        "category": "innovation",
        "question": "Tell me about a creative technical solution you devised for a problem that had no obvious answer.",
        "tips": [
            "Walk through your thought process, including the approaches you considered and rejected.",
            "Explain what made the final solution creative - an unusual combination of techniques, a novel use of an existing tool, or a reframing of the problem.",
            "Describe how you validated the solution would work before committing to a full implementation."
        ],
        "order_index": 22
    },
    {
        "category": "innovation",
        "question": "Describe a time you championed an internal developer experience improvement that was not on any product roadmap.",
        "tips": [
            "Explain how you made the case for investing in developer experience versus shipping product features.",
            "Describe the specific improvement - CI/CD pipeline, local development setup, observability tooling, or documentation.",
            "Show the impact on team velocity, developer satisfaction, or onboarding time for new engineers."
        ],
        "order_index": 23
    },
    {
        "category": "innovation",
        "question": "Tell me about a time you applied a concept or pattern from one domain to solve a problem in a completely different domain.",
        "tips": [
            "Explain the original domain where you learned the concept and why you saw the connection to the new problem.",
            "Describe how you adapted the idea to fit the new context rather than applying it blindly.",
            "Share whether the cross-pollination approach became a pattern others adopted."
        ],
        "order_index": 24
    },
    {
        "category": "innovation",
        "question": "Describe how you fostered a culture of experimentation and innovation within your team.",
        "tips": [
            "Give specific examples of structures you created - hack days, innovation sprints, 20% time, or structured experimentation frameworks.",
            "Describe how you handled failed experiments and made it safe to try things that might not work.",
            "Share examples of innovations that came out of this culture and made it into production."
        ],
        "order_index": 25
    },

    # ── Teamwork (7) ──
    {
        "category": "teamwork",
        "question": "Tell me about a time you collaborated with a team in a different time zone or geographic location on a critical deliverable.",
        "tips": [
            "Describe the specific communication and coordination practices you established to bridge the time zone gap.",
            "Explain how you ensured knowledge sharing and avoided bottlenecks when teams were not online simultaneously.",
            "Highlight the tools and async workflows you used to keep the project moving around the clock."
        ],
        "order_index": 26
    },
    {
        "category": "teamwork",
        "question": "Describe a time you had to onboard and ramp up a new team member quickly on a complex system.",
        "tips": [
            "Explain the onboarding plan you created, including documentation, pairing sessions, and starter tasks of increasing complexity.",
            "Describe how you balanced helping the new person with your own delivery responsibilities.",
            "Share how quickly the person became productive and what you would do differently next time."
        ],
        "order_index": 27
    },
    {
        "category": "teamwork",
        "question": "Tell me about a cross-functional project where you worked closely with product, design, and data teams.",
        "tips": [
            "Explain your role in bridging the gap between technical constraints and product or design aspirations.",
            "Describe how you ensured all disciplines had input into key decisions rather than engineering driving unilaterally.",
            "Share a specific example of a compromise or creative solution that emerged from the cross-functional collaboration."
        ],
        "order_index": 28
    },
    {
        "category": "teamwork",
        "question": "Describe a situation where you stepped outside your defined role to help the team succeed.",
        "tips": [
            "Explain what you noticed that was falling through the cracks and why you chose to pick it up.",
            "Describe the work you did - whether it was project management, testing, documentation, or customer support.",
            "Show that you did this without neglecting your primary responsibilities or creating confusion about ownership."
        ],
        "order_index": 29
    },
    {
        "category": "teamwork",
        "question": "Tell me about a time you helped two team members who were struggling to work together effectively.",
        "tips": [
            "Describe how you diagnosed the root cause of the friction - personality clash, unclear roles, or different working styles.",
            "Explain the specific interventions you made, such as facilitating a direct conversation or restructuring how they collaborated.",
            "Share whether the working relationship improved and what you learned about team dynamics."
        ],
        "order_index": 30
    },
    {
        "category": "teamwork",
        "question": "Describe how you contributed to a project where you were not the technical lead but had deep domain expertise.",
        "tips": [
            "Show that you supported the lead's decisions while sharing your expertise constructively.",
            "Describe specific moments where your domain knowledge prevented a mistake or unlocked a better approach.",
            "Explain how you managed your ego and focused on the team's success rather than your own visibility."
        ],
        "order_index": 31
    },
    {
        "category": "teamwork",
        "question": "Tell me about a time you built a high-performing engineering team from scratch or transformed an underperforming one.",
        "tips": [
            "Describe the hiring criteria you established and the culture you intentionally cultivated.",
            "Explain the processes and rituals you put in place - standups, retrospectives, architecture reviews, or pair programming.",
            "Share specific evidence of the team's performance improvement, such as delivery velocity, quality metrics, or retention."
        ],
        "order_index": 32
    },

    # ── Communication (6) ──
    {
        "category": "communication",
        "question": "Tell me about a time you had to explain a complex technical concept to a non-technical executive audience.",
        "tips": [
            "Describe how you tailored the explanation using analogies, visuals, or business impact framing rather than technical jargon.",
            "Show that you understood what the audience cared about and connected the technical topic to their concerns.",
            "Mention the outcome - did the executive make a different decision, approve a budget, or gain confidence in the technical direction?"
        ],
        "order_index": 33
    },
    {
        "category": "communication",
        "question": "Describe a time you wrote a technical design document or RFC that influenced a major architectural decision.",
        "tips": [
            "Explain the structure and content of the document, including alternatives considered and trade-off analysis.",
            "Describe the review and feedback process and how you incorporated input from other engineers.",
            "Show that the document served as a lasting reference, not just a one-time proposal."
        ],
        "order_index": 34
    },
    {
        "category": "communication",
        "question": "Tell me about a time you had to deliver difficult news to your team, such as a project cancellation, layoffs, or a major pivot.",
        "tips": [
            "Describe how you prepared for the conversation and anticipated people's reactions and concerns.",
            "Show that you were honest and transparent while being empathetic about the impact on individuals.",
            "Explain how you helped the team move forward constructively after delivering the news."
        ],
        "order_index": 35
    },
    {
        "category": "communication",
        "question": "Describe how you communicated the progress and risks of a complex project to multiple stakeholder groups with different interests.",
        "tips": [
            "Explain how you tailored the message and level of detail for each audience - executives, product managers, and engineers.",
            "Describe the cadence and format of updates you provided - dashboards, weekly summaries, or ad-hoc check-ins.",
            "Show an example of how transparent risk communication helped the project rather than causing panic."
        ],
        "order_index": 36
    },
    {
        "category": "communication",
        "question": "Tell me about a time you gave constructive feedback to a senior peer that changed their approach.",
        "tips": [
            "Describe how you chose the right time and setting for the feedback conversation.",
            "Explain how you framed the feedback around specific observations and impact rather than personal criticism.",
            "Share how the peer received the feedback and what changed as a result."
        ],
        "order_index": 37
    },
    {
        "category": "communication",
        "question": "Describe a situation where miscommunication led to a significant problem and how you resolved it.",
        "tips": [
            "Be specific about what was miscommunicated - a requirement, a deadline, a dependency, or an assumption.",
            "Explain how you diagnosed the root cause of the miscommunication.",
            "Describe the process or communication structure you put in place to prevent similar issues."
        ],
        "order_index": 38
    },

    # ── Decision Making (6) ──
    {
        "category": "decision_making",
        "question": "Tell me about a time you had to make a critical technical decision with incomplete information.",
        "tips": [
            "Explain what information was missing and what you did to reduce uncertainty - spikes, prototypes, expert consultations, or data analysis.",
            "Describe the framework you used to make the decision, such as reversibility analysis, risk-weighted outcomes, or time-boxing.",
            "Show that you established checkpoints to revisit the decision as new information became available."
        ],
        "order_index": 39
    },
    {
        "category": "decision_making",
        "question": "Describe a build-versus-buy decision you led and the reasoning behind your recommendation.",
        "tips": [
            "Explain the evaluation criteria you used - total cost of ownership, maintenance burden, customization needs, and strategic fit.",
            "Describe the stakeholders you consulted and how you balanced engineering preferences with business constraints.",
            "Share the outcome after implementation and whether the decision held up over time."
        ],
        "order_index": 40
    },
    {
        "category": "decision_making",
        "question": "Tell me about a time you decided to take on significant technical debt intentionally and how you managed it.",
        "tips": [
            "Explain the business pressure that justified taking on the debt and how you quantified the trade-off.",
            "Describe how you documented the debt and created a plan to pay it down.",
            "Show that you followed through on the paydown plan rather than letting the debt accumulate indefinitely."
        ],
        "order_index": 41
    },
    {
        "category": "decision_making",
        "question": "Describe a time you had to choose between two viable technical approaches and the trade-offs you weighed.",
        "tips": [
            "Explain the criteria that mattered most - performance, maintainability, team familiarity, time to market, or cost.",
            "Describe how you evaluated the options - benchmarks, prototypes, or consultation with domain experts.",
            "Show that you documented the decision and the reasoning so future engineers would understand the context."
        ],
        "order_index": 42
    },
    {
        "category": "decision_making",
        "question": "Tell me about a time you decided to deprecate or sunset a system or feature that people were still using.",
        "tips": [
            "Explain the analysis that led to the deprecation decision - maintenance cost, usage data, or better alternatives.",
            "Describe the migration plan you created and how you communicated timelines and support to affected users.",
            "Show that you handled edge cases and holdout users with patience rather than forcing a hard cutoff."
        ],
        "order_index": 43
    },
    {
        "category": "decision_making",
        "question": "Describe a time you reversed a decision you had previously championed because new evidence emerged.",
        "tips": [
            "Show intellectual honesty by explaining what changed your mind and why the original decision was reasonable at the time.",
            "Describe how you communicated the reversal to avoid eroding trust or confidence in your judgment.",
            "Explain what you learned about decision-making processes from the experience."
        ],
        "order_index": 44
    },

    # ── Growth (6) ──
    {
        "category": "growth",
        "question": "Tell me about a time you had to learn a new technology or domain quickly to deliver on a critical project.",
        "tips": [
            "Describe your learning strategy - reading documentation, building prototypes, finding a mentor, or studying existing codebases.",
            "Show that you were productive within a specific timeframe and did not let the learning curve delay the project significantly.",
            "Explain how you balanced learning depth with delivery speed and where you drew the line on good enough understanding."
        ],
        "order_index": 45
    },
    {
        "category": "growth",
        "question": "Describe how you transitioned from an individual contributor focus to a technical leadership role.",
        "tips": [
            "Explain the specific challenges of letting go of hands-on coding and shifting to influence, strategy, and people.",
            "Describe the habits and practices you developed to be effective in the new role.",
            "Share a specific example of a leadership win that you could not have achieved as a pure individual contributor."
        ],
        "order_index": 46
    },
    {
        "category": "growth",
        "question": "Tell me about feedback you received that fundamentally changed how you work.",
        "tips": [
            "Be specific about the feedback and who gave it rather than being vague about a general growth area.",
            "Describe your initial reaction honestly, especially if it was defensive, and how you processed it.",
            "Show concrete behavioral changes that resulted and how you verified the improvement."
        ],
        "order_index": 47
    },
    {
        "category": "growth",
        "question": "Describe a time you took on a stretch assignment or role that was outside your comfort zone.",
        "tips": [
            "Explain why the assignment was a stretch - unfamiliar domain, larger scope, or a skill you had not exercised before.",
            "Describe the support system you built - mentors, peers, or learning resources - to increase your chances of success.",
            "Share what you discovered about your capabilities and where you still see room for growth."
        ],
        "order_index": 48
    },
    {
        "category": "growth",
        "question": "Tell me about how you stay current with evolving technologies and industry trends.",
        "tips": [
            "Give specific examples of sources, communities, or practices - conferences, open source contributions, reading groups, or side projects.",
            "Describe how you filter signal from noise and decide which trends are worth investing time in.",
            "Show an example of how staying current directly benefited your team or a project."
        ],
        "order_index": 49
    },
    {
        "category": "growth",
        "question": "Describe a time you identified a gap in your own skills and proactively developed a plan to close it.",
        "tips": [
            "Be specific about the skill gap - distributed systems knowledge, public speaking, financial modeling, or people management.",
            "Describe the structured plan you followed, including timelines, resources, and accountability mechanisms.",
            "Show evidence that you closed the gap, such as successfully applying the skill in a real project."
        ],
        "order_index": 50
    },
]

# ======================================================================
# QUIZ DATA
# ======================================================================

QUIZZES = [
    # -------------------------------------------------------------------------
    # Lesson 0: Collections Framework Deep Dive
    # -------------------------------------------------------------------------
    {
        "lesson_index": 0,
        "question": "What is the default initial capacity and load factor of a Java HashMap?",
        "options": [
            "Initial capacity 8, load factor 0.5",
            "Initial capacity 16, load factor 0.75",
            "Initial capacity 32, load factor 0.75",
            "Initial capacity 16, load factor 0.5",
        ],
        "correct_index": 1,
        "explanation": "HashMap uses an initial capacity of 16 buckets and a load factor of 0.75. When the number of entries exceeds capacity * loadFactor (i.e. 12), the map resizes to double its capacity and rehashes all entries.",
    },
    {
        "lesson_index": 0,
        "question": "Which collection should you use when you need O(log n) ordered access with no duplicates and thread safety is not required?",
        "options": [
            "HashSet",
            "LinkedHashSet",
            "TreeSet",
            "ConcurrentSkipListSet",
        ],
        "correct_index": 2,
        "explanation": "TreeSet is backed by a TreeMap (a red-black tree) providing O(log n) add, remove, and contains operations while maintaining elements in sorted order. ConcurrentSkipListSet also provides ordered access but adds unnecessary thread-safety overhead when not needed.",
    },
    {
        "lesson_index": 0,
        "question": "What happens when two keys produce the same hash bucket in a Java 8+ HashMap?",
        "options": [
            "The second key overwrites the first",
            "An exception is thrown",
            "Entries form a linked list, converting to a balanced tree when the bucket exceeds 8 entries",
            "The map immediately doubles in size",
        ],
        "correct_index": 2,
        "explanation": "In Java 8+, HashMap handles collisions by chaining entries in a linked list. When a single bucket grows beyond the TREEIFY_THRESHOLD of 8 entries (and the table has at least 64 buckets), the linked list is converted to a red-black tree for O(log n) lookup instead of O(n).",
    },
    # -------------------------------------------------------------------------
    # Lesson 1: Concurrency - Thread Safety, Locks, and Executors
    # -------------------------------------------------------------------------
    {
        "lesson_index": 1,
        "question": "What is the key difference between ReentrantLock and synchronized in Java?",
        "options": [
            "ReentrantLock is always faster than synchronized",
            "ReentrantLock supports try-lock with timeout, interruptible locking, and fairness policies",
            "synchronized supports condition variables but ReentrantLock does not",
            "There is no practical difference; they are interchangeable",
        ],
        "correct_index": 1,
        "explanation": "ReentrantLock provides advanced features like tryLock() with a timeout, lockInterruptibly() for responding to interrupts, and an optional fairness policy that grants the lock to the longest-waiting thread. synchronized is simpler but lacks these capabilities.",
    },
    {
        "lesson_index": 1,
        "question": "Which ExecutorService method allows you to submit a batch of tasks and wait for all of them to complete?",
        "options": [
            "execute()",
            "submit()",
            "invokeAll()",
            "invokeAny()",
        ],
        "correct_index": 2,
        "explanation": "invokeAll() accepts a collection of Callable tasks, executes them all, and blocks until every task has completed (or the timeout expires). invokeAny() returns as soon as one task succeeds, and submit() returns a single Future without waiting.",
    },
    # -------------------------------------------------------------------------
    # Lesson 2: JVM Internals - Memory Model and Garbage Collection
    # -------------------------------------------------------------------------
    {
        "lesson_index": 2,
        "question": "In the Java Memory Model, what does the volatile keyword guarantee?",
        "options": [
            "Atomicity for compound operations like i++",
            "Visibility of changes across threads and prevents instruction reordering around the volatile access",
            "Mutual exclusion equivalent to synchronized",
            "That the variable is stored only on the stack, not the heap",
        ],
        "correct_index": 1,
        "explanation": "The volatile keyword establishes a happens-before relationship: a write to a volatile field is visible to all subsequent reads of that field by other threads. It also prevents the compiler and CPU from reordering instructions around the volatile access. However, it does not guarantee atomicity for compound operations.",
    },
    {
        "lesson_index": 2,
        "question": "Which garbage collector is designed for low-latency applications with pause times typically under 10ms, even on large heaps?",
        "options": [
            "Parallel GC",
            "CMS (Concurrent Mark Sweep)",
            "G1 GC",
            "ZGC",
        ],
        "correct_index": 3,
        "explanation": "ZGC (Z Garbage Collector) is designed for sub-millisecond to single-digit millisecond pause times regardless of heap size. It performs most of its work concurrently using colored pointers and load barriers. G1 targets pause times of around 200ms by default, and Parallel GC optimizes for throughput, not latency.",
    },
    {
        "lesson_index": 2,
        "question": "What happens during a 'Stop-the-World' event in JVM garbage collection?",
        "options": [
            "Only the garbage collector thread is paused",
            "All application threads are suspended while the GC performs its work",
            "The JVM writes a heap dump to disk",
            "The JVM switches from interpreted to compiled code",
        ],
        "correct_index": 1,
        "explanation": "During a Stop-the-World (STW) pause, all application threads are halted so the garbage collector can safely identify and reclaim unreachable objects without interference. Modern collectors like ZGC and Shenandoah minimize STW pauses by performing most GC work concurrently with application threads.",
    },
    # -------------------------------------------------------------------------
    # Lesson 3: Dependency Injection and Inversion of Control
    # -------------------------------------------------------------------------
    {
        "lesson_index": 3,
        "question": "In Spring, what is the recommended way to inject dependencies in production code?",
        "options": [
            "Field injection with @Autowired",
            "Setter injection with @Autowired",
            "Constructor injection (with or without @Autowired on the constructor)",
            "Static factory methods",
        ],
        "correct_index": 2,
        "explanation": "Constructor injection is the recommended approach because it makes dependencies explicit, supports immutability via final fields, and ensures the object is fully initialized before use. Since Spring 4.3, @Autowired is optional on a single constructor.",
    },
    {
        "lesson_index": 3,
        "question": "What scope does a Spring bean have by default?",
        "options": [
            "prototype - a new instance per injection point",
            "singleton - one shared instance per application context",
            "request - one instance per HTTP request",
            "session - one instance per HTTP session",
        ],
        "correct_index": 1,
        "explanation": "By default, Spring beans are singletons scoped to the ApplicationContext. This means one instance is created and shared across all injection points. The prototype scope creates a new instance each time the bean is requested, but you must explicitly declare it with @Scope(\"prototype\").",
    },
    # -------------------------------------------------------------------------
    # Lesson 4: Aspect-Oriented Programming and Proxies
    # -------------------------------------------------------------------------
    {
        "lesson_index": 4,
        "question": "Why does calling a @Transactional method from within the same class not trigger the transactional behavior?",
        "options": [
            "The @Transactional annotation is not inherited",
            "Self-invocation bypasses the proxy; the call goes directly to the target object",
            "Spring does not support @Transactional on private methods",
            "The transaction manager has not been configured",
        ],
        "correct_index": 1,
        "explanation": "Spring AOP works through proxies that wrap the target bean. When a method within the same class calls another method on 'this', it bypasses the proxy entirely, so the AOP advice (including @Transactional) is never triggered. To work around this, inject the bean into itself or extract the method into a separate bean.",
    },
    {
        "lesson_index": 4,
        "question": "What is the difference between JDK dynamic proxies and CGLIB proxies in Spring?",
        "options": [
            "JDK proxies are faster; CGLIB proxies are more feature-rich",
            "JDK proxies work on interfaces; CGLIB proxies subclass the target class",
            "CGLIB proxies require the target to implement an interface; JDK proxies do not",
            "There is no difference; Spring always uses CGLIB",
        ],
        "correct_index": 1,
        "explanation": "JDK dynamic proxies create a proxy that implements the same interfaces as the target bean, so they require the bean to implement at least one interface. CGLIB proxies generate a subclass of the target class at runtime, which works for concrete classes but cannot proxy final classes or final methods.",
    },
    # -------------------------------------------------------------------------
    # Lesson 5: Spring Security with JWT Authentication
    # -------------------------------------------------------------------------
    {
        "lesson_index": 5,
        "question": "In a JWT-based authentication flow, where should the token typically be stored on the client side for a web application?",
        "options": [
            "In a cookie with HttpOnly and Secure flags",
            "In localStorage for easy JavaScript access",
            "In a URL query parameter",
            "In the HTML meta tag",
        ],
        "correct_index": 0,
        "explanation": "Storing JWTs in HttpOnly cookies prevents JavaScript access (mitigating XSS attacks) while the Secure flag ensures transmission only over HTTPS. localStorage is vulnerable to XSS since any script on the page can read it. URL parameters risk token leakage through browser history and server logs.",
    },
    {
        "lesson_index": 5,
        "question": "What is the primary purpose of the refresh token in a JWT authentication scheme?",
        "options": [
            "To encrypt the access token payload",
            "To allow obtaining a new access token without re-authenticating with credentials",
            "To store additional user claims that do not fit in the access token",
            "To validate the access token signature on the server",
        ],
        "correct_index": 1,
        "explanation": "Refresh tokens allow clients to obtain new short-lived access tokens without requiring the user to log in again. Access tokens are kept short-lived (minutes) to limit exposure if compromised, while refresh tokens are longer-lived and stored securely, typically rotated on each use.",
    },
    # -------------------------------------------------------------------------
    # Lesson 6: Decorators and Metaclasses
    # -------------------------------------------------------------------------
    {
        "lesson_index": 6,
        "question": "What does functools.wraps do when applied to a wrapper function inside a decorator?",
        "options": [
            "It makes the decorator thread-safe",
            "It copies the original function's __name__, __doc__, and other attributes to the wrapper",
            "It caches the return value of the decorated function",
            "It converts the decorator into a class-based decorator",
        ],
        "correct_index": 1,
        "explanation": "functools.wraps preserves the decorated function's metadata (__name__, __module__, __doc__, __qualname__, __annotations__) on the wrapper. Without it, introspection tools, documentation generators, and debuggers would see the wrapper's name instead of the original function's name.",
    },
    {
        "lesson_index": 6,
        "question": "In Python, when is a metaclass's __new__ method called?",
        "options": [
            "Each time an instance of the class is created",
            "When the class body itself is being created (i.e., when the class statement is executed)",
            "When the module is imported for the first time",
            "Only when type() is called explicitly",
        ],
        "correct_index": 1,
        "explanation": "A metaclass's __new__ is invoked when the class object itself is being constructed, which happens when the interpreter processes the class statement. This is distinct from the class's own __new__, which is called when creating instances of that class. Metaclasses control the creation of classes, not instances.",
    },
    # -------------------------------------------------------------------------
    # Lesson 7: Async Programming with asyncio
    # -------------------------------------------------------------------------
    {
        "lesson_index": 7,
        "question": "What is the fundamental difference between asyncio.gather() and asyncio.wait()?",
        "options": [
            "gather() runs tasks sequentially; wait() runs them concurrently",
            "gather() returns results in input order and raises on first exception by default; wait() returns sets of done/pending tasks",
            "wait() is deprecated in favor of gather()",
            "gather() supports timeouts; wait() does not",
        ],
        "correct_index": 1,
        "explanation": "asyncio.gather() returns results as a list in the same order as the input awaitables and by default propagates the first exception. asyncio.wait() returns two sets (done and pending) and gives more control over completion conditions (FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED) and timeouts.",
    },
    {
        "lesson_index": 7,
        "question": "Why should you avoid calling blocking I/O functions directly inside an async coroutine?",
        "options": [
            "Blocking I/O is not supported in Python 3.7+",
            "It blocks the single event loop thread, preventing all other coroutines from making progress",
            "It causes a RuntimeError in asyncio",
            "Blocking calls automatically become non-blocking inside async functions",
        ],
        "correct_index": 1,
        "explanation": "asyncio uses a single-threaded event loop. If a coroutine calls a blocking function (like time.sleep or a synchronous HTTP request), it blocks the entire event loop, starving all other coroutines. Use loop.run_in_executor() to offload blocking calls to a thread pool, or use async-native libraries.",
    },
    # -------------------------------------------------------------------------
    # Lesson 8: Big-O Notation and Complexity Analysis
    # -------------------------------------------------------------------------
    {
        "lesson_index": 8,
        "question": "What is the time complexity of searching for an element in a balanced binary search tree?",
        "options": [
            "O(1)",
            "O(log n)",
            "O(n)",
            "O(n log n)",
        ],
        "correct_index": 1,
        "explanation": "In a balanced BST, each comparison eliminates roughly half the remaining nodes, giving O(log n) time complexity. An unbalanced BST can degrade to O(n) in the worst case, which is why self-balancing variants like AVL trees and red-black trees are preferred in practice.",
    },
    {
        "lesson_index": 8,
        "question": "Which of the following represents the tightest upper bound for the time complexity of sorting n elements using comparison-based sorting?",
        "options": [
            "O(n)",
            "O(n log n)",
            "O(n^2)",
            "O(2^n)",
        ],
        "correct_index": 1,
        "explanation": "The information-theoretic lower bound for comparison-based sorting is Omega(n log n), proven by the decision tree argument. Algorithms like merge sort and heapsort achieve O(n log n) in the worst case, making it both the lower and upper bound for optimal comparison-based sorts.",
    },
    {
        "lesson_index": 8,
        "question": "An algorithm has the recurrence T(n) = 2T(n/2) + O(n). What is its time complexity?",
        "options": [
            "O(n)",
            "O(n log n)",
            "O(n^2)",
            "O(log n)",
        ],
        "correct_index": 1,
        "explanation": "By the Master Theorem (case 2), when T(n) = aT(n/b) + O(n^d) and log_b(a) = d, the complexity is O(n^d log n). Here a=2, b=2, d=1, and log_2(2)=1=d, giving O(n log n). This is the same recurrence as merge sort.",
    },
    # -------------------------------------------------------------------------
    # Lesson 9: Trees and Binary Search Trees
    # -------------------------------------------------------------------------
    {
        "lesson_index": 9,
        "question": "What is the worst-case height of an AVL tree with n nodes?",
        "options": [
            "O(n)",
            "O(log n)",
            "O(sqrt(n))",
            "O(n log n)",
        ],
        "correct_index": 1,
        "explanation": "AVL trees maintain a balance factor of at most 1 between the heights of left and right subtrees at every node. This strict balancing guarantees the height is always O(log n), specifically about 1.44 * log2(n). This ensures O(log n) search, insert, and delete operations.",
    },
    {
        "lesson_index": 9,
        "question": "Which traversal of a binary search tree visits nodes in ascending order?",
        "options": [
            "Pre-order (root, left, right)",
            "In-order (left, root, right)",
            "Post-order (left, right, root)",
            "Level-order (breadth-first)",
        ],
        "correct_index": 1,
        "explanation": "In-order traversal visits the left subtree, then the root, then the right subtree. Because the BST property ensures all left descendants are smaller and all right descendants are larger, in-order traversal naturally produces nodes in sorted (ascending) order.",
    },
    # -------------------------------------------------------------------------
    # Lesson 10: Graph Algorithms - BFS, DFS, and Shortest Paths
    # -------------------------------------------------------------------------
    {
        "lesson_index": 10,
        "question": "When should you use Dijkstra's algorithm instead of BFS for shortest paths?",
        "options": [
            "When the graph is unweighted",
            "When the graph has weighted edges with non-negative weights",
            "When the graph contains negative weight cycles",
            "When you only need to check reachability",
        ],
        "correct_index": 1,
        "explanation": "BFS finds shortest paths in unweighted graphs (or graphs where all edges have equal weight). Dijkstra's algorithm extends this to graphs with non-negative edge weights using a priority queue. For graphs with negative edges (but no negative cycles), Bellman-Ford is required.",
    },
    {
        "lesson_index": 10,
        "question": "What is the time complexity of BFS on a graph represented as an adjacency list with V vertices and E edges?",
        "options": [
            "O(V)",
            "O(E)",
            "O(V + E)",
            "O(V * E)",
        ],
        "correct_index": 2,
        "explanation": "BFS visits each vertex at most once (O(V)) and examines each edge at most once via the adjacency list (O(E)), giving O(V + E) total. With an adjacency matrix, it would be O(V^2) since checking all potential neighbors of each vertex takes O(V).",
    },
    # -------------------------------------------------------------------------
    # Lesson 11: CAP Theorem and Consistency Models
    # -------------------------------------------------------------------------
    {
        "lesson_index": 11,
        "question": "According to the CAP theorem, during a network partition, a distributed system must choose between which two properties?",
        "options": [
            "Consistency and Availability",
            "Consistency and Partition tolerance",
            "Availability and Performance",
            "Performance and Partition tolerance",
        ],
        "correct_index": 0,
        "explanation": "The CAP theorem states that during a network partition (which is inevitable in distributed systems), a system must choose between Consistency (all nodes see the same data) and Availability (every request receives a response). Partition tolerance is not optional in real distributed systems.",
    },
    {
        "lesson_index": 11,
        "question": "What does 'eventual consistency' guarantee?",
        "options": [
            "All reads return the most recent write immediately",
            "If no new updates are made, all replicas will eventually converge to the same value",
            "Data is always consistent across at least two replicas",
            "Writes are acknowledged only after all replicas are updated",
        ],
        "correct_index": 1,
        "explanation": "Eventual consistency guarantees convergence: if no new writes occur, all replicas will eventually return the same value. It does not specify how long convergence takes. Systems like DynamoDB and Cassandra offer eventual consistency for high availability, with optional stronger consistency modes for critical reads.",
    },
    {
        "lesson_index": 11,
        "question": "Which consistency model does a system provide if every read returns the most recent write or an error?",
        "options": [
            "Eventual consistency",
            "Causal consistency",
            "Strong (linearizable) consistency",
            "Read-your-writes consistency",
        ],
        "correct_index": 2,
        "explanation": "Linearizable (strong) consistency ensures that every read reflects the most recently completed write, as if there were a single copy of the data. This is the strongest guarantee but comes at the cost of higher latency and lower availability during partitions, as described by the CAP theorem.",
    },
    # -------------------------------------------------------------------------
    # Lesson 12: Caching Strategies and Patterns
    # -------------------------------------------------------------------------
    {
        "lesson_index": 12,
        "question": "In a cache-aside (lazy loading) pattern, when does the cache get populated?",
        "options": [
            "Before the application starts, during a warm-up phase",
            "On every write operation",
            "On a cache miss - the application reads from the database and writes the result to the cache",
            "The cache is never explicitly populated; it mirrors the database in real time",
        ],
        "correct_index": 2,
        "explanation": "In cache-aside, the application first checks the cache. On a miss, it reads from the database, stores the result in the cache, and returns it. This means the first request for any data always hits the database, and only subsequently accessed data is cached. It avoids caching data that is never read.",
    },
    {
        "lesson_index": 12,
        "question": "What problem does the write-behind (write-back) caching pattern solve, and what risk does it introduce?",
        "options": [
            "It ensures strong consistency but increases read latency",
            "It reduces write latency by batching writes to the database asynchronously, but risks data loss on cache failure",
            "It prevents cache stampedes but doubles storage requirements",
            "It eliminates stale reads but requires two-phase commit",
        ],
        "correct_index": 1,
        "explanation": "Write-behind caching writes to the cache immediately and asynchronously flushes changes to the database in batches. This dramatically reduces write latency and database load but introduces a window where data exists only in the cache. If the cache node fails before flushing, those writes are lost.",
    },
    # -------------------------------------------------------------------------
    # Lesson 13: Consensus Algorithms - Paxos and Raft
    # -------------------------------------------------------------------------
    {
        "lesson_index": 13,
        "question": "In Raft consensus, what is the minimum number of nodes that must agree for a value to be committed in a 5-node cluster?",
        "options": [
            "2",
            "3",
            "4",
            "5",
        ],
        "correct_index": 1,
        "explanation": "Raft requires a majority quorum for commits. In a 5-node cluster, the majority is ceil(5/2) + 1 = 3 nodes (including the leader). This ensures that any two quorums overlap by at least one node, preventing conflicting commits. The cluster can tolerate up to 2 node failures.",
    },
    {
        "lesson_index": 13,
        "question": "What is the primary role of the leader in the Raft consensus protocol?",
        "options": [
            "To detect network partitions and trigger re-elections",
            "To serialize all client requests and replicate log entries to followers",
            "To maintain a backup copy of the state machine",
            "To balance load across follower nodes",
        ],
        "correct_index": 1,
        "explanation": "In Raft, the leader handles all client requests, appends them to its log, and replicates entries to followers via AppendEntries RPCs. Once a majority acknowledges, the entry is committed. This single-leader design simplifies the protocol compared to multi-leader approaches like Multi-Paxos.",
    },
    # -------------------------------------------------------------------------
    # Lesson 14: Event Sourcing and CQRS
    # -------------------------------------------------------------------------
    {
        "lesson_index": 14,
        "question": "What is the primary advantage of event sourcing over traditional CRUD-based persistence?",
        "options": [
            "Lower storage costs since events are smaller than full records",
            "Complete audit trail and the ability to rebuild state to any point in time",
            "Faster read queries due to pre-computed views",
            "Simpler application code with fewer data models",
        ],
        "correct_index": 1,
        "explanation": "Event sourcing stores every state change as an immutable event. This provides a complete audit trail, enables temporal queries (what was the state at time T?), and allows replaying events to rebuild projections or fix bugs. The trade-off is increased complexity and eventual consistency between the event store and read models.",
    },
    {
        "lesson_index": 14,
        "question": "In CQRS, why are the command and query models separated?",
        "options": [
            "To enforce different security policies on reads and writes",
            "To allow independent optimization and scaling of the read and write sides",
            "To reduce the number of database tables",
            "To eliminate the need for a message broker",
        ],
        "correct_index": 1,
        "explanation": "CQRS separates the write model (optimized for business rules and consistency) from the read model (optimized for query patterns and denormalization). This allows each side to scale independently - for example, using many read replicas for heavy read loads while keeping the write side focused on correctness.",
    },
    # -------------------------------------------------------------------------
    # Lesson 15: AWS Lambda and Serverless Architecture
    # -------------------------------------------------------------------------
    {
        "lesson_index": 15,
        "question": "What is a 'cold start' in AWS Lambda and how can you mitigate it?",
        "options": [
            "A failed invocation that returns a 500 error; mitigate with retry policies",
            "The initial latency when a new execution environment is provisioned; mitigate with provisioned concurrency",
            "A timeout caused by exceeding the 15-minute limit; mitigate with Step Functions",
            "The delay in deploying a new Lambda version; mitigate with aliases",
        ],
        "correct_index": 1,
        "explanation": "A cold start occurs when Lambda must create a new execution environment (download code, start the runtime, run initialization). This adds latency ranging from 100ms to several seconds depending on runtime and package size. Provisioned concurrency keeps environments warm and eliminates cold starts for latency-sensitive workloads.",
    },
    {
        "lesson_index": 15,
        "question": "What is the maximum execution duration for a single AWS Lambda invocation?",
        "options": [
            "5 minutes",
            "10 minutes",
            "15 minutes",
            "60 minutes",
        ],
        "correct_index": 2,
        "explanation": "AWS Lambda functions have a maximum timeout of 15 minutes (900 seconds). For workloads that need longer execution, consider AWS Step Functions to orchestrate multiple Lambda invocations, or use ECS/Fargate for long-running tasks.",
    },
    # -------------------------------------------------------------------------
    # Lesson 16: SQS and Event-Driven Architecture
    # -------------------------------------------------------------------------
    {
        "lesson_index": 16,
        "question": "What is the key difference between Amazon SQS Standard and FIFO queues?",
        "options": [
            "Standard queues have unlimited throughput; FIFO queues are limited to 3,000 messages/second with batching",
            "Standard queues guarantee ordering; FIFO queues guarantee deduplication only",
            "FIFO queues support dead-letter queues; Standard queues do not",
            "Standard queues support messages up to 256KB; FIFO queues support up to 1MB",
        ],
        "correct_index": 0,
        "explanation": "SQS Standard queues offer nearly unlimited throughput with best-effort ordering and at-least-once delivery. FIFO queues guarantee exactly-once processing and strict message ordering within message groups, but are limited to 300 messages/second (3,000 with batching). Choose based on whether ordering and deduplication matter.",
    },
    {
        "lesson_index": 16,
        "question": "What is the purpose of a dead-letter queue (DLQ) in SQS?",
        "options": [
            "To store messages that have been successfully processed for auditing",
            "To capture messages that could not be processed after a configured number of receive attempts",
            "To prioritize high-priority messages over low-priority ones",
            "To encrypt messages at rest",
        ],
        "correct_index": 1,
        "explanation": "A DLQ receives messages that have exceeded the maxReceiveCount - the maximum number of times a consumer can receive (and fail to process) a message. This prevents poison messages from blocking the queue indefinitely and allows operators to inspect and debug failed messages separately.",
    },
    # -------------------------------------------------------------------------
    # Lesson 17: Azure Kubernetes Service (AKS) Deep Dive
    # -------------------------------------------------------------------------
    {
        "lesson_index": 17,
        "question": "What is the purpose of a Kubernetes Horizontal Pod Autoscaler (HPA)?",
        "options": [
            "To increase the size of individual pods when they run out of memory",
            "To automatically scale the number of pod replicas based on observed CPU/memory utilization or custom metrics",
            "To distribute pods evenly across all available nodes",
            "To restart unhealthy pods automatically",
        ],
        "correct_index": 1,
        "explanation": "The HPA automatically adjusts the number of pod replicas in a deployment based on observed metrics like CPU utilization, memory usage, or custom metrics from Prometheus. It scales out (adds pods) when demand increases and scales in when demand drops, maintaining the target utilization.",
    },
    {
        "lesson_index": 17,
        "question": "In AKS, what is the difference between a node pool and a pod?",
        "options": [
            "A node pool is a set of VMs with the same configuration; a pod is the smallest deployable unit containing one or more containers",
            "A node pool is a namespace; a pod is a deployment",
            "A node pool manages networking; a pod manages storage",
            "There is no difference; they are synonyms",
        ],
        "correct_index": 0,
        "explanation": "A node pool is a group of Azure VMs with identical configuration (VM size, OS, etc.) that serve as worker nodes in the AKS cluster. A pod is the smallest deployable unit in Kubernetes, wrapping one or more containers that share networking and storage. Pods are scheduled onto nodes within node pools.",
    },
    # -------------------------------------------------------------------------
    # Lesson 18: Kafka Fundamentals - Topics, Partitions, and Offsets
    # -------------------------------------------------------------------------
    {
        "lesson_index": 18,
        "question": "In Kafka, what determines which partition a message is sent to?",
        "options": [
            "The broker with the least load receives it",
            "Messages are always sent round-robin across partitions",
            "If a key is provided, a hash of the key determines the partition; otherwise, round-robin or sticky partitioning is used",
            "The consumer group decides the target partition",
        ],
        "correct_index": 2,
        "explanation": "When a message has a key, Kafka's default partitioner hashes the key (murmur2) and maps it to a partition, ensuring all messages with the same key go to the same partition. Without a key, the producer uses sticky partitioning (batching to one partition before rotating) for efficiency. Custom partitioners can override this behavior.",
    },
    {
        "lesson_index": 18,
        "question": "What happens when a new consumer joins an existing Kafka consumer group?",
        "options": [
            "Nothing; it starts consuming from a new topic",
            "A rebalance occurs, redistributing partition assignments among all consumers in the group",
            "The new consumer waits until an existing consumer disconnects",
            "All consumers restart from offset zero",
        ],
        "correct_index": 1,
        "explanation": "When a consumer joins or leaves a group, Kafka triggers a rebalance. The group coordinator reassigns partitions so each partition is consumed by exactly one consumer in the group. During rebalance, consumption pauses briefly. Cooperative rebalancing (incremental) minimizes this disruption compared to the eager protocol.",
    },
    {
        "lesson_index": 18,
        "question": "What is the maximum number of active consumers that can read from a topic with 6 partitions in a single consumer group?",
        "options": [
            "1",
            "3",
            "6",
            "Unlimited",
        ],
        "correct_index": 2,
        "explanation": "Each partition is assigned to exactly one consumer within a consumer group. With 6 partitions, at most 6 consumers can be active. A 7th consumer would sit idle. To increase parallelism, increase the number of partitions. Different consumer groups can independently consume from all partitions.",
    },
    # -------------------------------------------------------------------------
    # Lesson 19: Exactly-Once Semantics and Kafka Transactions
    # -------------------------------------------------------------------------
    {
        "lesson_index": 19,
        "question": "What does Kafka's idempotent producer guarantee?",
        "options": [
            "Messages are delivered in order across all partitions",
            "Exactly-once delivery to a single partition by deduplicating retries using sequence numbers",
            "Messages are encrypted end-to-end",
            "The producer waits for all replicas before acknowledging",
        ],
        "correct_index": 1,
        "explanation": "An idempotent producer assigns a monotonically increasing sequence number to each message per partition. If a retry sends a duplicate (due to a network glitch after a successful write), the broker detects the duplicate sequence number and discards it, guaranteeing exactly-once delivery per partition.",
    },
    {
        "lesson_index": 19,
        "question": "What is the 'read_committed' isolation level in Kafka consumers?",
        "options": [
            "Consumers can only read messages from committed Kafka transactions, not aborted ones",
            "Consumers acknowledge every message immediately",
            "Consumers read messages only after all replicas have been updated",
            "Consumers can read messages from any topic regardless of ACLs",
        ],
        "correct_index": 0,
        "explanation": "With isolation.level=read_committed, a consumer only sees messages from committed transactions and non-transactional messages. Messages from aborted transactions are filtered out. This is essential for end-to-end exactly-once semantics in consume-transform-produce patterns.",
    },
    # -------------------------------------------------------------------------
    # Lesson 20: Redis Data Structures and Caching Patterns
    # -------------------------------------------------------------------------
    {
        "lesson_index": 20,
        "question": "Which Redis data structure is most efficient for implementing a leaderboard with ranked scores?",
        "options": [
            "List",
            "Hash",
            "Sorted Set (ZSET)",
            "Set",
        ],
        "correct_index": 2,
        "explanation": "Redis Sorted Sets store members with associated scores and maintain them in sorted order. ZADD, ZRANK, ZRANGE, and ZREVRANGE provide O(log n) operations for adding, ranking, and retrieving ranges. This makes sorted sets ideal for leaderboards, priority queues, and time-series secondary indexes.",
    },
    {
        "lesson_index": 20,
        "question": "What is the 'cache stampede' (thundering herd) problem, and how can it be mitigated?",
        "options": [
            "Too many keys in the cache causing memory overflow; mitigate with LRU eviction",
            "Many clients simultaneously requesting an expired key, all hitting the database; mitigate with locking or probabilistic early expiration",
            "Cache nodes failing due to high write throughput; mitigate with write-behind",
            "Data inconsistency between cache and database; mitigate with TTL",
        ],
        "correct_index": 1,
        "explanation": "A cache stampede occurs when a popular key expires and many concurrent requests all find a cache miss, flooding the database with identical queries. Mitigation strategies include mutex/locking (only one request rebuilds the cache), probabilistic early expiration (XFetch), and never-expire patterns with background refresh.",
    },
    {
        "lesson_index": 20,
        "question": "What is the difference between Redis EXPIRE and EXPIREAT commands?",
        "options": [
            "EXPIRE sets a TTL in seconds relative to now; EXPIREAT sets an absolute Unix timestamp",
            "EXPIRE removes the key immediately; EXPIREAT schedules removal",
            "EXPIRE works on strings only; EXPIREAT works on all data types",
            "There is no difference; they are aliases",
        ],
        "correct_index": 0,
        "explanation": "EXPIRE sets a time-to-live in seconds from the current moment (e.g., EXPIRE key 300 for 5 minutes). EXPIREAT takes an absolute Unix timestamp (e.g., EXPIREAT key 1700000000). Both result in the key being automatically deleted when the time arrives. PEXPIRE and PEXPIREAT offer millisecond precision.",
    },
    # -------------------------------------------------------------------------
    # Lesson 21: Driving Technical Strategy and the RFC Process
    # -------------------------------------------------------------------------
    {
        "lesson_index": 21,
        "question": "What is the primary purpose of an RFC (Request for Comments) in an engineering organization?",
        "options": [
            "To get management approval for a project's budget",
            "To document a proposed technical decision, gather feedback from stakeholders, and build consensus before implementation",
            "To assign tasks to individual engineers",
            "To replace code reviews for large changes",
        ],
        "correct_index": 1,
        "explanation": "An RFC is a written proposal that describes a technical problem, explores alternatives, recommends a solution, and invites structured feedback. It surfaces risks early, builds shared understanding, creates a decision record, and ensures stakeholders across teams can contribute before significant engineering effort is invested.",
    },
    {
        "lesson_index": 21,
        "question": "When driving technical alignment across teams, what is the most effective first step?",
        "options": [
            "Presenting your fully designed solution in an all-hands meeting",
            "Understanding each team's constraints, priorities, and concerns through 1:1 conversations before proposing a solution",
            "Escalating to leadership to mandate alignment",
            "Writing a detailed specification and sending it via email",
        ],
        "correct_index": 1,
        "explanation": "Effective alignment starts with listening. By having 1:1 conversations with stakeholders from each team, you understand their constraints and can incorporate their concerns into your proposal. This creates buy-in before the formal review, reduces resistance, and produces a stronger solution informed by diverse perspectives.",
    },
    {
        "lesson_index": 21,
        "question": "What should an RFC document include to be most effective?",
        "options": [
            "Only the recommended solution with implementation details",
            "The problem statement, alternatives considered with trade-offs, the recommended approach, and a rollback plan",
            "A Gantt chart with timelines and resource allocation",
            "Source code for the proposed changes",
        ],
        "correct_index": 1,
        "explanation": "A strong RFC includes: context and problem statement (why), alternatives considered with pros/cons (what else), the recommended approach with rationale (what and why), success metrics, risks and mitigations, and a rollback plan. Showing alternatives demonstrates thorough thinking and gives reviewers confidence in the recommendation.",
    },
]


# ======================================================================
# SEED FUNCTION
# ======================================================================


def seed_all():
    """Seed the database with all sample content. Skips if data already exists."""
    db = SessionLocal()
    try:
        existing = db.query(Lesson).first()
        if existing:
            print("Database already seeded - skipping.")
            return

        print("Seeding lessons...")
        lesson_objects = []
        for data in LESSONS:
            lesson = Lesson(
                category=data["category"],
                title=data["title"],
                slug=data["slug"],
                difficulty=data["difficulty"],
                order_index=data["order_index"],
                content=data["content"],
                examples=data["examples"],
                exercises=data["exercises"],
                tags=data["tags"],
            )
            db.add(lesson)
            lesson_objects.append(lesson)
        db.flush()

        print("Seeding quizzes...")
        for data in QUIZZES:
            lesson = lesson_objects[data["lesson_index"]]
            quiz = Quiz(
                lesson_id=lesson.id,
                question=data["question"],
                options=data["options"],
                correct_index=data["correct_index"],
                explanation=data["explanation"],
            )
            db.add(quiz)

        print("Seeding system design problems...")
        for data in SYSTEM_DESIGN_PROBLEMS:
            problem = SystemDesignProblem(
                title=data["title"],
                slug=data["slug"],
                difficulty=data["difficulty"],
                category=data["category"],
                description=data["description"],
                requirements=data["requirements"],
                estimation_hints=data["estimation_hints"],
                api_design=data["api_design"],
                schema_design=data["schema_design"],
                scaling_notes=data["scaling_notes"],
                failure_modes=data["failure_modes"],
                trade_offs=data["trade_offs"],
                diagram_description=data["diagram_description"],
                order_index=data["order_index"],
            )
            db.add(problem)

        print("Seeding coding problems...")
        all_coding = CODING_PROBLEMS_1 + CODING_PROBLEMS_2
        for data in all_coding:
            problem = CodingProblem(
                title=data["title"],
                slug=data["slug"],
                difficulty=data["difficulty"],
                category=data["category"],
                description=data["description"],
                examples=data["examples"],
                constraints=data["constraints"],
                hints=data["hints"],
                solution_java=data["solution_java"],
                solution_python=data["solution_python"],
                test_cases=data["test_cases"],
                time_complexity=data["time_complexity"],
                space_complexity=data["space_complexity"],
                order_index=data["order_index"],
            )
            db.add(problem)

        print("Seeding STAR questions...")
        for data in STAR_QUESTIONS:
            question = StarQuestion(
                category=data["category"],
                question=data["question"],
                tips=data["tips"],
                order_index=data["order_index"],
            )
            db.add(question)

        db.commit()
        print(
            f"Seeding complete: {len(LESSONS)} lessons, {len(QUIZZES)} quizzes, "
            f"{len(SYSTEM_DESIGN_PROBLEMS)} system design problems, "
            f"{len(all_coding)} coding problems, {len(STAR_QUESTIONS)} STAR questions."
        )
    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()

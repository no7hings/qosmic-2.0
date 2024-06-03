
```JavaScript
const targetYear = 2024
const targetMonth = 5 // 例如，5 表示五月

const prompt = `LIST WITHOUT ID 
file.name + " : " + 
started.year + "-" + started.month + "-" + started.day +
", " + 
finished.year + "-" + finished.month + "-" + finished.day
FROM #task_progress
WHERE date(finished).year = ${targetYear} AND date(finished).month = ${targetMonth}
SORT finished desc`

const mermaidConf = `mermaid
gantt
    title Book Reading Chart for ${targetYear}-${targetMonth}
    dateFormat  YYYY-M-D
    axisFormat  %d
    todaymarker off`

// 执行查询并获取结果
const te = await dv.queryMarkdown(prompt)

// 调试输出查询结果
console.log(te)

if (!te || !te.value) {
    dv.paragraph("Error: No data returned from query.")
} else {
    // 去掉前缀并生成甘特图
    const prefixedList = te.value

    // 转换日期格式为 YYYY-MMDD
    const formattedList = prefixedList.replaceAll(/\b(\d{4})-(\d{2})-(\d{2})\b/g, '$1-$2$3')

    const list = formattedList.replaceAll(/^-\s/gm, "")
    const backticks = "```"

    dv.paragraph(
        `${backticks}${mermaidConf}
${list}
${backticks} 
    `,
    )
}
```

```JavaScript
const targetYear = 2024

const prompt = `LIST WITHOUT ID 
file.name + " : " + 
started.year + "-" + started.month + "-" + started.day +
", " + 
finished.year + "-" + finished.month + "-" + finished.day
FROM #task_progress
WHERE date(finished).year = ${targetYear}
SORT finished desc`

const mermaidConf = `mermaid
gantt
    title 任务进度 ${targetYear}
    dateFormat  YYYY-M-D
    axisFormat  %B
    todaymarker off`

// 执行查询并获取结果
const te = await dv.queryMarkdown(prompt)

// 调试输出查询结果
console.log(te)

if (!te || !te.value) {
    dv.paragraph("Error: No data returned from query.")
} else {
    // 去掉前缀并生成甘特图
    const prefixedList = te.value
    const list = prefixedList.replaceAll(/^-\s/gm, "")
    const backticks = "```"

    dv.paragraph(
        `${backticks}${mermaidConf}
${list}
${backticks} 
    `,
    )
}
```
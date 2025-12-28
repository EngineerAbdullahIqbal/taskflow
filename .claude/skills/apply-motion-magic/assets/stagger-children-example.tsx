// BEFORE: Static list
export function TaskList({ tasks }: TaskListProps) {
  return (
    <ul className="space-y-2">
      {tasks.map((task) => (
        <li key={task.id} className="p-4 bg-zinc-900 rounded">
          <h4>{task.title}</h4>
          <p>{task.description}</p>
        </li>
      ))}
    </ul>
  )
}

// AFTER: Animated with StaggerChildren
import { motion } from 'motion/react'

// Parent stagger configuration
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1 // 100ms delay between each child
    }
  }
}

// Child animation
const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.3 }
  }
}

export function TaskList({ tasks }: TaskListProps) {
  return (
    <motion.ul 
      className="space-y-2"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      {tasks.map((task) => (
        <motion.li 
          key={task.id} 
          className="p-4 bg-zinc-900 rounded"
          variants={itemVariants} // No need for initial/animate on children
        >
          <h4>{task.title}</h4>
          <p>{task.description}</p>
        </motion.li>
      ))}
    </motion.ul>
  )
}

// Key Pattern: Parent has staggerChildren, children just have variants.
// Motion automatically orchestrates the timing.

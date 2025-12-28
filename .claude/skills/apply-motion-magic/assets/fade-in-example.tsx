// BEFORE: Static component
export function Card({ title, description }: CardProps) {
  return (
    <div className="p-6 bg-zinc-900 rounded-lg">
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  )
}

// AFTER: Animated with FadeIn
import { motion } from 'motion/react'

const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } }
}

export function Card({ title, description }: CardProps) {
  return (
    <motion.div 
      className="p-6 bg-zinc-900 rounded-lg"
      initial="hidden"
      animate="visible"
      variants={fadeIn}
    >
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </motion.div>
  )
}

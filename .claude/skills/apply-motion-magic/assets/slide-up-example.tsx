// BEFORE: Static section
export function FeatureSection({ features }: FeatureSectionProps) {
  return (
    <section className="py-20">
      <h2 className="text-3xl font-bold mb-12">Features</h2>
      <div className="grid gap-6 md:grid-cols-3">
        {features.map((feature) => (
          <div key={feature.id} className="p-6 bg-zinc-900/50 rounded-lg">
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

// AFTER: Animated with SlideUp
import { motion } from 'motion/react'

const slideUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4 } }
}

export function FeatureSection({ features }: FeatureSectionProps) {
  return (
    <motion.section 
      className="py-20"
      initial="hidden"
      animate="visible"
      variants={slideUp}
    >
      <h2 className="text-3xl font-bold mb-12">Features</h2>
      <div className="grid gap-6 md:grid-cols-3">
        {features.map((feature) => (
          <motion.div 
            key={feature.id} 
            className="p-6 bg-zinc-900/50 rounded-lg"
            variants={slideUp}
          >
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </motion.div>
        ))}
      </div>
    </motion.section>
  )
}

// BEFORE: Static buttons
import { Button } from '@/components/ui/button'
import { ArrowRight, Download } from 'lucide-react'

export function CTASection() {
  return (
    <div className="flex gap-4">
      <Button size="lg" className="group">
        Get Started
        <ArrowRight className="ml-2" />
      </Button>
      <Button size="lg" variant="outline">
        <Download className="mr-2" />
        Download
      </Button>
    </div>
  )
}

// AFTER: Animated with gestures
import { motion } from 'motion/react'
import { Button } from '@/components/ui/button'
import { ArrowRight, Download } from 'lucide-react'

// Wrap Button with motion for gestures
const MotionButton = motion.create(Button)

export function CTASection() {
  return (
    <div className="flex gap-4">
      <MotionButton 
        size="lg" 
        className="group"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        transition={{ duration: 0.15 }}
      >
        Get Started
        <motion.div
          className="ml-2 inline-block"
          animate={{ x: [0, 4, 0] }}
          transition={{ repeat: Infinity, duration: 1.5 }}
        >
          <ArrowRight />
        </motion.div>
      </MotionButton>
      
      <MotionButton 
        size="lg" 
        variant="outline"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        transition={{ duration: 0.15 }}
      >
        <Download className="mr-2" />
        Download
      </MotionButton>
    </div>
  )
}

// Pattern: Use motion.create() to wrap custom components like shadcn Button
// whileHover: Triggered on pointer enter
// whileTap: Triggered on click/touch
// Always use GPU properties (scale, x, y) for 60fps performance

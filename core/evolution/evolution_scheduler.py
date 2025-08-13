#!/usr/bin/env python3
"""
Evolution Scheduler - Phase 6 Feature 2 Component
Background scheduling and execution of evolution tasks
"""

import os
import json
import time
import threading
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict
import queue
import heapq

logger = logging.getLogger(__name__)

@dataclass
class ScheduledTask:
    """Scheduled evolution task with priority queue support"""
    priority: int  # Lower number = higher priority
    scheduled_time: float
    task_id: str
    task_type: str
    task_data: Dict[str, Any]
    status: str = 'scheduled'
    created_at: float = None
    
    def __lt__(self, other):
        """Priority queue comparison - lower priority number = higher priority"""
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.scheduled_time < other.scheduled_time

class EvolutionScheduler:
    """Schedules and coordinates evolution processes with background processing"""
    
    def __init__(self, evolution_engine):
        self.evolution_engine = evolution_engine
        
        # Task management
        self.evolution_tasks = []
        self.scheduled_tasks = []
        self.running_tasks = {}
        self.completed_tasks = []
        self.failed_tasks = []
        
        # Priority mapping
        self.priority_map = {
            'low': 4,
            'normal': 3,
            'high': 2,
            'critical': 1
        }
        
        # Background processing
        self.scheduler_thread = None
        self.scheduler_active = False
        self.executor_thread = None
        self.executor_active = False
        
        # Task execution
        self.max_concurrent_tasks = 3
        self.task_timeout = 300  # 5 minutes
        self.retry_attempts = 3
        
        # Statistics
        self.scheduler_stats = {
            'total_scheduled': 0,
            'total_executed': 0,
            'total_completed': 0,
            'total_failed': 0,
            'average_execution_time': 0.0,
            'last_execution': 0
        }
        
        # Task queues
        self.high_priority_queue = queue.PriorityQueue()
        self.normal_priority_queue = queue.Queue()
        self.low_priority_queue = queue.Queue()
        
        logger.info("📅 Evolution Scheduler initialized")
    
    def start_background_scheduling(self):
        """Start background scheduling process"""
        if self.scheduler_active:
            logger.warning("⚠️ Evolution scheduler already active")
            return False
        
        try:
            self.scheduler_active = True
            
            # Start scheduler thread
            self.scheduler_thread = threading.Thread(
                target=self._scheduling_loop,
                daemon=True,
                name="EvolutionScheduler"
            )
            self.scheduler_thread.start()
            
            # Start executor thread
            self.executor_thread = threading.Thread(
                target=self._execution_loop,
                daemon=True,
                name="EvolutionExecutor"
            )
            self.executor_thread.start()
            
            logger.info("📅 Evolution scheduler started in background")
            return True
            
        except Exception as e:
            logger.error(f"Error starting evolution scheduler: {str(e)}")
            self.scheduler_active = False
            return False
    
    def stop_background_scheduling(self):
        """Stop background scheduling process"""
        try:
            self.scheduler_active = False
            self.executor_active = False
            
            # Wait for threads to finish
            if self.scheduler_thread and self.scheduler_thread.is_alive():
                self.scheduler_thread.join(timeout=5)
            
            if self.executor_thread and self.executor_thread.is_alive():
                self.executor_thread.join(timeout=5)
            
            logger.info("📅 Evolution scheduler stopped")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping evolution scheduler: {str(e)}")
            return False
    
    def schedule_evolution_task(self, task_data: Dict[str, Any]) -> str:
        """Schedule an evolution task with intelligent prioritization"""
        try:
            # Generate task ID
            task_id = f"evolution_{int(time.time())}_{hash(str(task_data)) % 10000}"
            
            # Determine priority
            priority_str = task_data.get('priority', 'normal')
            priority = self.priority_map.get(priority_str, 3)
            
            # Calculate scheduled time
            delay = task_data.get('delay', 0)
            scheduled_time = time.time() + delay
            
            # Create scheduled task
            scheduled_task = ScheduledTask(
                priority=priority,
                scheduled_time=scheduled_time,
                task_id=task_id,
                task_type=task_data.get('type', 'performance'),
                task_data=task_data,
                created_at=time.time()
            )
            
            # Add to appropriate queue based on priority
            if priority <= 2:  # High or critical priority
                self.high_priority_queue.put(scheduled_task)
            elif priority == 3:  # Normal priority
                self.normal_priority_queue.put(scheduled_task)
            else:  # Low priority
                self.low_priority_queue.put(scheduled_task)
            
            # Update statistics
            self.scheduler_stats['total_scheduled'] += 1
            
            logger.info(f"📅 Evolution task scheduled: {task_id} ({task_data.get('type', 'unknown')}, priority: {priority_str})")
            
            return task_id
            
        except Exception as e:
            logger.error(f"Error scheduling evolution task: {str(e)}")
            return None
    
    def _scheduling_loop(self):
        """Background scheduling loop"""
        logger.info("📅 Evolution scheduling loop started")
        
        while self.scheduler_active:
            try:
                current_time = time.time()
                
                # Check high priority queue
                self._process_priority_queue(self.high_priority_queue, current_time)
                
                # Check normal priority queue
                self._process_priority_queue(self.normal_priority_queue, current_time)
                
                # Check low priority queue
                self._process_priority_queue(self.low_priority_queue, current_time)
                
                # Sleep briefly
                time.sleep(1)  # Check every second
                
            except Exception as e:
                logger.error(f"Evolution scheduling error: {str(e)}")
                time.sleep(5)  # Wait 5 seconds before retrying
        
        logger.info("📅 Evolution scheduling loop ended")
    
    def _process_priority_queue(self, task_queue: queue.Queue, current_time: float):
        """Process tasks in a priority queue"""
        try:
            # Check if we can execute more tasks
            if len(self.running_tasks) >= self.max_concurrent_tasks:
                return
            
            # Get next task from queue
            if not task_queue.empty():
                scheduled_task = task_queue.get_nowait()
                
                # Check if task is ready to execute
                if scheduled_task.scheduled_time <= current_time:
                    # Check if we have capacity
                    if len(self.running_tasks) < self.max_concurrent_tasks:
                        # Execute task
                        self._execute_evolution_task(scheduled_task)
                    else:
                        # Put task back in queue for later
                        task_queue.put(scheduled_task)
                else:
                    # Task not ready yet, put back in queue
                    task_queue.put(scheduled_task)
                    
        except queue.Empty:
            pass  # Queue is empty, continue
        except Exception as e:
            logger.error(f"Error processing priority queue: {str(e)}")
    
    def _execution_loop(self):
        """Background execution loop"""
        logger.info("⚡ Evolution execution loop started")
        self.executor_active = True
        
        while self.executor_active:
            try:
                # Check for completed tasks
                self._check_completed_tasks()
                
                # Check for timed out tasks
                self._check_timed_out_tasks()
                
                # Sleep briefly
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                logger.error(f"Evolution execution error: {str(e)}")
                time.sleep(5)  # Wait 5 seconds before retrying
        
        logger.info("⚡ Evolution execution loop ended")
    
    def _execute_evolution_task(self, scheduled_task: ScheduledTask):
        """Execute an evolution task"""
        try:
            # Mark task as running
            scheduled_task.status = 'running'
            self.running_tasks[scheduled_task.task_id] = {
                'task': scheduled_task,
                'started_at': time.time(),
                'attempts': 0
            }
            
            # Update statistics
            self.scheduler_stats['total_executed'] += 1
            self.scheduler_stats['last_execution'] = time.time()
            
            logger.info(f"⚡ Executing evolution task: {scheduled_task.task_id} ({scheduled_task.task_type})")
            
            # Execute the task based on type
            result = self._execute_task_by_type(scheduled_task)
            
            # Mark task as completed
            if result.get('success', False):
                scheduled_task.status = 'completed'
                self.completed_tasks.append({
                    'task': scheduled_task,
                    'result': result,
                    'execution_time': time.time() - self.running_tasks[scheduled_task.task_id]['started_at']
                })
                self.scheduler_stats['total_completed'] += 1
                logger.info(f"✅ Evolution task completed: {scheduled_task.task_id}")
            else:
                scheduled_task.status = 'failed'
                self.failed_tasks.append({
                    'task': scheduled_task,
                    'error': result.get('error', 'Unknown error'),
                    'attempts': self.running_tasks[scheduled_task.task_id]['attempts']
                })
                self.scheduler_stats['total_failed'] += 1
                logger.error(f"❌ Evolution task failed: {scheduled_task.task_id}")
            
            # Remove from running tasks
            if scheduled_task.task_id in self.running_tasks:
                del self.running_tasks[scheduled_task.task_id]
            
        except Exception as e:
            logger.error(f"Error executing evolution task: {str(e)}")
            scheduled_task.status = 'failed'
            scheduled_task.error = str(e)
            
            # Move to failed tasks
            self.failed_tasks.append({
                'task': scheduled_task,
                'error': str(e),
                'attempts': 0
            })
            
            # Remove from running tasks
            if scheduled_task.task_id in self.running_tasks:
                del self.running_tasks[scheduled_task.task_id]
    
    def _execute_task_by_type(self, scheduled_task: ScheduledTask) -> Dict[str, Any]:
        """Execute a task based on its type"""
        try:
            task_type = scheduled_task.task_type
            task_data = scheduled_task.task_data
            
            # Execute based on task type
            if task_type == 'performance':
                return self._execute_performance_evolution(task_data)
            elif task_type == 'efficiency':
                return self._execute_efficiency_evolution(task_data)
            elif task_type == 'intelligence':
                return self._execute_intelligence_evolution(task_data)
            elif task_type == 'adaptability':
                return self._execute_adaptability_evolution(task_data)
            else:
                return {
                    'success': False,
                    'error': f'Unknown task type: {task_type}',
                    'result': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Task execution error: {str(e)}',
                'result': None
            }
    
    def _execute_performance_evolution(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute performance evolution task"""
        try:
            # Simulate performance evolution
            evolution_result = {
                'type': 'performance',
                'improvement': 0.05,  # 5% improvement
                'metrics': {
                    'response_time': -10,  # 10ms improvement
                    'throughput': 0.08,    # 8% improvement
                    'efficiency': 0.03     # 3% improvement
                }
            }
            
            # Update system health
            self._update_system_health('performance', evolution_result['improvement'])
            
            return {
                'success': True,
                'result': evolution_result,
                'message': 'Performance evolution completed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Performance evolution failed: {str(e)}',
                'result': None
            }
    
    def _execute_efficiency_evolution(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute efficiency evolution task"""
        try:
            # Simulate efficiency evolution
            evolution_result = {
                'type': 'efficiency',
                'improvement': 0.03,  # 3% improvement
                'metrics': {
                    'resource_usage': -0.05,  # 5% reduction
                    'energy_efficiency': 0.04, # 4% improvement
                    'optimization_rate': 0.06  # 6% improvement
                }
            }
            
            # Update system health
            self._update_system_health('efficiency', evolution_result['improvement'])
            
            return {
                'success': True,
                'result': evolution_result,
                'message': 'Efficiency evolution completed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Efficiency evolution failed: {str(e)}',
                'result': None
            }
    
    def _execute_intelligence_evolution(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute intelligence evolution task"""
        try:
            # Simulate intelligence evolution
            evolution_result = {
                'type': 'intelligence',
                'improvement': 0.04,  # 4% improvement
                'metrics': {
                    'learning_rate': 0.05,    # 5% improvement
                    'pattern_recognition': 0.06, # 6% improvement
                    'decision_accuracy': 0.03   # 3% improvement
                }
            }
            
            # Update system health
            self._update_system_health('intelligence', evolution_result['improvement'])
            
            return {
                'success': True,
                'result': evolution_result,
                'message': 'Intelligence evolution completed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Intelligence evolution failed: {str(e)}',
                'result': None
            }
    
    def _execute_adaptability_evolution(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute adaptability evolution task"""
        try:
            # Simulate adaptability evolution
            evolution_result = {
                'type': 'adaptability',
                'improvement': 0.06,  # 6% improvement
                'metrics': {
                    'adaptation_speed': 0.07,   # 7% improvement
                    'flexibility': 0.05,        # 5% improvement
                    'resilience': 0.04          # 4% improvement
                }
            }
            
            # Update system health
            self._update_system_health('adaptability', evolution_result['improvement'])
            
            return {
                'success': True,
                'result': evolution_result,
                'message': 'Adaptability evolution completed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Adaptability evolution failed: {str(e)}',
                'result': None
            }
    
    def _update_system_health(self, health_type: str, improvement: float):
        """Update system health based on evolution results"""
        try:
            # Get current system health
            system_health = self.evolution_engine.get_system_health()
            
            # Update the specific health score
            if health_type == 'performance':
                system_health.performance_score = min(1.0, system_health.performance_score + improvement)
            elif health_type == 'efficiency':
                system_health.efficiency_score = min(1.0, system_health.efficiency_score + improvement)
            elif health_type == 'intelligence':
                system_health.intelligence_score = min(1.0, system_health.intelligence_score + improvement)
            elif health_type == 'adaptability':
                system_health.adaptability_score = min(1.0, system_health.adaptability_score + improvement)
            
            logger.info(f"📊 Updated {health_type} health score: +{improvement:.3f}")
            
        except Exception as e:
            logger.error(f"Error updating system health: {str(e)}")
    
    def _check_completed_tasks(self):
        """Check for completed tasks and update statistics"""
        try:
            # Update average execution time
            if self.completed_tasks:
                total_time = sum(task['execution_time'] for task in self.completed_tasks)
                self.scheduler_stats['average_execution_time'] = total_time / len(self.completed_tasks)
                
        except Exception as e:
            logger.error(f"Error checking completed tasks: {str(e)}")
    
    def _check_timed_out_tasks(self):
        """Check for timed out tasks"""
        try:
            current_time = time.time()
            timed_out_tasks = []
            
            for task_id, task_info in self.running_tasks.items():
                if current_time - task_info['started_at'] > self.task_timeout:
                    timed_out_tasks.append(task_id)
            
            # Handle timed out tasks
            for task_id in timed_out_tasks:
                task_info = self.running_tasks[task_id]
                task = task_info['task']
                
                # Increment attempts
                task_info['attempts'] += 1
                
                if task_info['attempts'] >= self.retry_attempts:
                    # Task failed after max attempts
                    task.status = 'failed'
                    task.error = 'Task timed out after maximum retry attempts'
                    self.failed_tasks.append({
                        'task': task,
                        'error': 'Task timed out after maximum retry attempts',
                        'attempts': task_info['attempts']
                    })
                    self.scheduler_stats['total_failed'] += 1
                    logger.error(f"⏰ Task timed out after {task_info['attempts']} attempts: {task_id}")
                    
                    # Remove from running tasks
                    del self.running_tasks[task_id]
                else:
                    # Retry task
                    logger.warning(f"🔄 Retrying timed out task: {task_id} (attempt {task_info['attempts']})")
                    # Reset start time for retry
                    task_info['started_at'] = current_time
                    
        except Exception as e:
            logger.error(f"Error checking timed out tasks: {str(e)}")
    
    def get_scheduler_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        try:
            # Calculate success rate
            total_executed = self.scheduler_stats['total_executed']
            success_rate = 0.0
            if total_executed > 0:
                success_rate = self.scheduler_stats['total_completed'] / total_executed
            
            stats = self.scheduler_stats.copy()
            stats['success_rate'] = success_rate
            stats['current_running'] = len(self.running_tasks)
            stats['queue_sizes'] = {
                'high_priority': self.high_priority_queue.qsize(),
                'normal_priority': self.normal_priority_queue.qsize(),
                'low_priority': self.low_priority_queue.qsize()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting scheduler stats: {str(e)}")
            return {}
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a specific task"""
        try:
            # Check running tasks
            if task_id in self.running_tasks:
                task_info = self.running_tasks[task_id]
                return {
                    'task_id': task_id,
                    'status': 'running',
                    'started_at': task_info['started_at'],
                    'attempts': task_info['attempts'],
                    'elapsed_time': time.time() - task_info['started_at']
                }
            
            # Check completed tasks
            for completed_task in self.completed_tasks:
                if completed_task['task'].task_id == task_id:
                    return {
                        'task_id': task_id,
                        'status': 'completed',
                        'result': completed_task['result'],
                        'execution_time': completed_task['execution_time']
                    }
            
            # Check failed tasks
            for failed_task in self.failed_tasks:
                if failed_task['task'].task_id == task_id:
                    return {
                        'task_id': task_id,
                        'status': 'failed',
                        'error': failed_task['error'],
                        'attempts': failed_task['attempts']
                    }
            
            return {
                'task_id': task_id,
                'status': 'not_found',
                'error': 'Task not found in any queue or status'
            }
            
        except Exception as e:
            return {
                'task_id': task_id,
                'status': 'error',
                'error': str(e)
            }

# Main execution for testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create mock evolution engine for testing
    class MockEvolutionEngine:
        def get_system_health(self):
            from dataclasses import dataclass
            @dataclass
            class MockSystemHealth:
                performance_score: float = 0.7
                efficiency_score: float = 0.8
                intelligence_score: float = 0.6
                adaptability_score: float = 0.9
                overall_health: float = 0.75
                health_trend: str = 'stable'
                resource_usage: Dict[str, float] = None
                last_check: float = 0
            return MockSystemHealth()
    
    # Create scheduler
    evolution_engine = MockEvolutionEngine()
    scheduler = EvolutionScheduler(evolution_engine)
    
    try:
        # Start scheduler
        if scheduler.start_background_scheduling():
            logger.info("🚀 Scheduler started successfully")
            
            # Schedule some test tasks
            task1 = scheduler.schedule_evolution_task({
                'type': 'performance',
                'priority': 'high',
                'delay': 2
            })
            
            task2 = scheduler.schedule_evolution_task({
                'type': 'efficiency',
                'priority': 'normal',
                'delay': 5
            })
            
            task3 = scheduler.schedule_evolution_task({
                'type': 'intelligence',
                'priority': 'low',
                'delay': 10
            })
            
            logger.info(f"📅 Scheduled tasks: {task1}, {task2}, {task3}")
            
            # Keep running for a while to see task execution
            time.sleep(20)
            
            # Get statistics
            stats = scheduler.get_scheduler_stats()
            logger.info(f"📊 Scheduler stats: {stats}")
            
            # Stop scheduler
            scheduler.stop_background_scheduling()
            logger.info("🛑 Scheduler stopped successfully")
            
        else:
            logger.error("❌ Failed to start scheduler")
            
    except KeyboardInterrupt:
        logger.info("🛑 Interrupted by user")
        scheduler.stop_background_scheduling()
    except Exception as e:
        logger.error(f"❌ Error in main execution: {str(e)}")
        scheduler.stop_background_scheduling()

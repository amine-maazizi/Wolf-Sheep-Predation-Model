from threading import Lock

from config import *


class CollisionManager:
    # Thread-safe Singleton class
    
    instances = {}

    _lock: Lock = Lock() # lock object that will be used to synchronize threads during first access to the Singleton.
    
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
    
    def process_collisions(self, collisions):
        for entity in collisions.keys():
            for prospect in collisions.keys():
                if prospect != entity and collisions[entity].colliderect(collisions[prospect]):
                    self.resolve_collision(entity, prospect)

    def resolve_collision(self, entity, prospect):
        # Handles the physics aspect of the collision and runs handle_collision on each entity
        # to handle the simulation aspect of collisions
        
        # Calculate the overlap in both x and y directions
        overlap_x = min(entity.rect.right - prospect.rect.left, prospect.rect.right - entity.rect.left)
        overlap_y = min(entity.rect.bottom - prospect.rect.top, prospect.rect.bottom - entity.rect.top)
        
        push_back: int  = TILE_SIZE // 4
        
        if overlap_x < overlap_y:
            # Handle horizontal collision resolution
            if entity.rect.centerx < prospect.rect.centerx:
                # Entity is to the left of prospect, push entity to the left
                entity.rect.right = prospect.rect.left
                entity.rect.x -= push_back
                prospect.rect.x += push_back
            else:
                # Entity is to the right of prospect, push entity to the right
                entity.rect.left = prospect.rect.right
                entity.rect.x += push_back
                prospect.rect.x -= push_back
            # Reverse horizontal directions for both entities
            entity.direction.x = -entity.direction.x
            prospect.direction.x = -prospect.direction.x
        else:
            # Handle vertical collision resolution
            if entity.rect.centery < prospect.rect.centery:
                # Entity is above prospect, push entity up
                entity.rect.bottom = prospect.rect.top
                entity.rect.y -= push_back
                prospect.rect.y += push_back
            else:
                # Entity is below prospect, push entity down
                entity.rect.top = prospect.rect.bottom
                entity.rect.y += push_back
                prospect.rect.y -= push_back
            # Reverse vertical directions for both entities
            entity.direction.y = -entity.direction.y
            prospect.direction.y = -prospect.direction.y
        
        # Call handle_collision to process the logical aspects of the collision
        entity.handle_collision(prospect.type, prospect.gender)
        prospect.handle_collision(entity.type, entity.gender)
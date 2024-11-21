S_ALONE = 0
S_TALKING = 1

# ==============================================================================
# Group class:
# member fields:
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
# ==============================================================================

S_ALONE = 0
S_TALKING = 1

class Group:

    def __init__(self):
        self.members = {}
        self.chat_grps = {}
        self.grp_ever = 0

    def join(self, name):
        self.members[name] = S_ALONE
        return

    def is_member(self, name):

        # IMPLEMENTATION
        # ---- start your code ---- #
        if name in self.members:
            return True

        return False
        # ---- end of your code --- #

    # implement
    def leave(self, name):
        """
        leave the system, and the group
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        self.members.pop(name)
        for k in self.chat_grps:
            if name in self.chat_grps[k]:
                self.chat_grps[k].remove(name)
                if len(self.chat_grps[k]) == 1:
                    self.members[self.chat_grps[k][0]] = S_ALONE
                    self.chat_grps[k].clear()
                    self.chat_grps.pop(k)

        # ---- end of your code --- #
        return

    def find_group(self, name):
        """
        Auxiliary function internal to the class; return two
        variables: whether "name" is in a group, and if true
        the key to its group
        """

        found = False
        group_key = 0
        # IMPLEMENTATION
        # ---- start your code ---- #
        for keys in self.chat_grps:
            if name in self.chat_grps[keys]:
                found = True
                group_key = keys

        # ---- end of your code --- #
        return found, group_key

    def connect(self, me, peer):
        """
        me is alone, connecting peer.
        if peer is in a group, join it
        otherwise, create a new group with you and your peer
        """
        peer_in_group, group_key = self.find_group(peer)

        # IMPLEMENTATION
        # ---- start your code ---- #
        if peer_in_group:
            self.chat_grps[group_key].append(me)
        else:
            self.grp_ever+=1
            self.chat_grps[self.grp_ever] = [me,peer]
        self.members[me],self.members[peer] = S_TALKING, S_TALKING
        # ---- end of your code --- #
        return

    # implement
    def disconnect(self, me):
        """
        find myself in the group, quit, but stay in the system
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        me_in_group, group_key = self.find_group(me)
        if me_in_group:
            self.chat_grps[group_key].remove(me)
            if len(self.chat_grps[group_key]) == 1:
                self.members[self.chat_grps[group_key][0]] = S_ALONE
                self.chat_grps[group_key].clear()
                self.chat_grps.pop(group_key)
            self.members[me] = S_ALONE

        # ---- end of your code --- #
        return

    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        return full_list

    # implement
    def list_me(self, me):
        """
        return a list, "me" followed by other peers in my group
        """
        my_list = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        me_in_group, group_key = self.find_group(me)
        if me_in_group:
            my_list.extend(self.chat_grps[group_key])
            my_list.remove(me)
            my_list.insert(0, me)
        # ---- end of your code --- #
        return my_list


if __name__ == "__main__":
    g = Group()
    g.join('a')
    g.join('b')
    g.join('c')
    g.join('d')
    print(g.list_all())

    g.connect('a', 'b')
    print(g.list_all())
    g.connect('c', 'a')
    print(g.list_all())
    g.leave('c')
    print(g.list_all())
    g.disconnect('b')
    print(g.list_all())
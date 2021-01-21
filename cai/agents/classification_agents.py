# ------------------------------------------------------------------------------
# A group of cnn/classification agents.
# ------------------------------------------------------------------------------

from cai.agents.agent import Agent
import torch
import os
from torchvision import transforms
import numpy as np
<<<<<<< HEAD
from sklearn.metrics import accuracy_score
from cai.paths import telegram_login
from cai.utils.update_bots.telegram_bot import TelegramBot

#from cai.utils.agents.save_restore import save_state as external_save_state
#from cai.utils.agents.save_restore import restore_state as external_restore_state

class TransNetAgent(Agent):
    r"""An Agent for transfer learning models."""
=======
from cai.paths import telegram_login
from cai.utils.update_bots.telegram_bot import TelegramBot
from cai.utils.agents.save_restore import save_state as external_save_state
from cai.utils.agents.save_restore import restore_state as external_restore_state

class AlexNetAgent(Agent):
    r"""An Agent for AlexNet models."""
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = TelegramBot(telegram_login)

<<<<<<< HEAD
    def preprocess(self, img_tensor):
        r"""Transforms an image based on the desired input of
        transfer model.
=======
    def save_state(self, states_path, state_name, optimizer=None, overwrite=False,
                   losses_train=None, losses_val=None, accuracy_train=None,
                   accuracy_det_train=None, accuracy_val=None, accuracy_det_val=None,
                   path_npy_files=None):
        r"""Saves an agent state. Raises an error if the directory exists and 
        overwrite=False. Saves all further results like losses and accuracies as
        .npy files.
        """
        external_save_state(self, states_path, state_name, optimizer, overwrite,
                            losses_train, losses_val, accuracy_train,
                            accuracy_det_train, accuracy_val, accuracy_det_val,
                            path_npy_files)

    def restore_state(self, states_path, state_name, path_npy_files, optimizer=None):
        r"""Tries to restore a previous agent state, consisting of a model 
        state and the content of agent_state_dict. Returns whether the restore 
        operation  was successful. Further the results will be loaded as well,
        i.e. losses and accuracies.
        """
        return external_restore_state(self, states_path, state_name, path_npy_files, optimizer)

    def preprocess(self, img_tensor):
        r"""Transforms an image based on the desired input of
        AlexNet.
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
        """
        preprocess = transforms.Compose([
            transforms.ToPILImage(),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        batch_size = list(img_tensor.size())[0]
        new_img = preprocess(img_tensor[0].cpu().detach()).unsqueeze(0)
        for batch in range(1, batch_size):
            img = img_tensor[batch]
            img = preprocess(img.cpu().detach()).unsqueeze(0) # preprocess image and add batch dimension
            new_img = torch.cat((new_img, img), 0)
        return new_img.to(self.device)

    def train(self, optimizer, loss_f, train_dataloader,
              val_dataloader, nr_epochs=100, start_epoch=0, save_path=None,
<<<<<<< HEAD
              losses=list(), losses_cum=list(), losses_val=list(), losses_cum_val=list(),
              accuracy=list(), accuracy_detailed=list(), accuracy_val=list(),
              accuracy_val_detailed=list(), save_interval=10,
              msg_bot=True, bot_msg_interval=10):
=======
              save_interval=10, msg_bot=True, bot_msg_interval=10):
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
        r"""Train a model through its agent. Performs training epochs, 
        tracks metrics and saves model states.
        """
        assert start_epoch < nr_epochs, 'Start epoch needs to be smaller than the number of epochs!'
        if msg_bot == True:
            self.bot.send_msg('Start training the model for {} epochs..'.format(nr_epochs-start_epoch))
<<<<<<< HEAD
        
=======
        losses = list()
        losses_cum = list()
        losses_val = list()
        losses_cum_val = list()
        accuracy = list()
        accuracy_detailed = list()
        accuracy_val = list()
        accuracy_val_detailed = list()
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
        for epoch in range(start_epoch, nr_epochs):
            msg = "Running epoch "
            msg += str(epoch + 1) + " of " + str(nr_epochs) + "."
            print (msg, end = "\r")
            epoch_loss = list()
            results_y = list()
            results_yhat = list()
            total = 0
<<<<<<< HEAD
            acc = 0
            idxs = 0
            for idx, (x, y) in enumerate(train_dataloader):
                x, y = x.to(self.device), y.to(self.device)
                x = self.preprocess(x)
                yhat = self.model(x)
                loss = loss_f(yhat, y.float())
                total += y.size(0)
                mod_yhat = np.round(yhat.cpu().detach())
                acc += 100 * accuracy_score(y.cpu().detach().numpy(), mod_yhat)
                idxs += 1
                epoch_loss.append(loss.item())
                results_y.extend(y.cpu().detach().numpy().tolist())
                results_yhat.extend(mod_yhat.cpu().detach().numpy().tolist())
=======
            correct = 0
            for idx, (x, y) in enumerate(train_dataloader):
                x, y = x.to(self.device), y.to(self.device)
                x = self.replicating_image(x, 3)
                x = self.preprocess(x)
                yhat = self.model(x)
                loss = loss_f(yhat, torch.max(y, 1)[1])
                total += y.size(0)
                epoch_loss.append(loss.item())
                _, mod_yhat = torch.max(yhat, 1)
                _, labels = torch.max(y, 1)
                correct += (mod_yhat == labels).sum().item()
                results_y.extend(y.cpu().detach().numpy().tolist())
                results_yhat.extend(yhat.cpu().detach().numpy().tolist())
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            losses.append(epoch_loss)
            losses_cum.append([epoch+1, sum(epoch_loss) / total])
<<<<<<< HEAD
            accuracy.append([epoch+1, acc / idxs])
=======
            accuracy.append([epoch+1, 100 * correct / total])
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            accuracy_detailed.append(list(zip(results_y, results_yhat)))

            # Validate current model based on validation dataloader
            epoch_loss_val = list()
            results_y_val = list()
            results_yhat_val = list()
            results_mod_yhat_val = list()
            total_val = 0
<<<<<<< HEAD
            acc_val = 0
            idxs_val = 0
            with torch.no_grad():
                for idx, (x, y) in enumerate(val_dataloader):
                    x_val, y_val = x.to(self.device), y.to(self.device)
                    x_val = self.preprocess(x_val)
                    yhat_val = self.model(x_val)
                    loss = loss_f(yhat_val, y_val.float())
                    total_val += y_val.size(0)
                    epoch_loss_val.append(loss.item())
                    mod_yhat_val = np.round(yhat_val.cpu().detach())
                    acc_val += 100 * accuracy_score(y.cpu().detach().numpy(), mod_yhat_val)
                    idxs_val += 1
                    results_y_val.extend(y_val.cpu().detach().numpy().tolist())
                    results_yhat_val.extend(mod_yhat_val.cpu().detach().numpy().tolist())
                losses_val.append(epoch_loss_val)
                losses_cum_val.append([epoch+1, sum(epoch_loss_val) / total_val])
                accuracy_val.append([epoch+1, acc_val / idxs_val])
=======
            correct_val = 0
            with torch.no_grad():
                for idx, (x, y) in enumerate(val_dataloader):
                    x_val, y_val = x.to(self.device), y.to(self.device)
                    x_val = self.replicating_image(x_val, 3)
                    x_val = self.preprocess(x_val)
                    yhat_val = self.model(x_val)
                    loss = loss_f(yhat_val, torch.max(y_val, 1)[1])
                    total_val += y_val.size(0)
                    epoch_loss_val.append(loss.item())
                    _, mod_yhat_val = torch.max(yhat_val, 1)
                    _, labels_val = torch.max(y_val, 1)
                    correct_val += (mod_yhat_val == labels_val).sum().item()
                    results_y_val.extend(y_val.cpu().detach().numpy().tolist())
                    results_yhat_val.extend(yhat_val.cpu().detach().numpy().tolist())
                losses_val.append(epoch_loss_val)
                losses_cum_val.append([epoch+1, sum(epoch_loss_val) / total_val])
                accuracy_val.append([epoch+1, 100 * correct_val / total_val])
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
                accuracy_val_detailed.append(list(zip(results_y_val, results_yhat_val)))

            print(('Epoch --> Loss --> Accuracy: {} --> {:.4} --> {:.4}%.\n'
                   'Val_Loss --> Val_Accuracy: {:.4} --> {:.4}%.').format(epoch + 1,
                                                    sum(epoch_loss) / total,
<<<<<<< HEAD
                                                    acc / idxs,
                                                    sum(epoch_loss_val) / total_val,
                                                    acc_val / idxs_val))
=======
                                                    100 * correct / total,
                                                    sum(epoch_loss_val) / total_val,
                                                    100 * correct_val / total_val))
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            if (epoch + 1) % bot_msg_interval == 0 and msg_bot:
                self.bot.send_msg(('Epoch --> Loss --> Accuracy: {} --> {:.4} --> {:.4}%.\n'
                                   'Val_Loss --> Val_Accuracy: {:.4} --> {:.4}%.').format(epoch + 1,
                                                                    sum(epoch_loss) / total,
<<<<<<< HEAD
                                                                    acc / idxs,
                                                                    sum(epoch_loss_val) / total_val,
                                                                    acc_val / idxs_val))
=======
                                                                    100 * correct / total,
                                                                    sum(epoch_loss_val) / total_val,
                                                                    100 * correct_val / total_val))
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            # Save agent and optimizer state
            if (epoch + 1) % save_interval == 0 and save_path is not None:
                print('Saving current state after epoch: {}.'.format(epoch + 1))
                self.save_state(save_path, 'epoch_{}'.format(epoch + 1),
<<<<<<< HEAD
                                optimizer, True, losses, losses_cum, losses_val,
                                losses_cum_val, accuracy, accuracy_detailed, accuracy_val,
                                accuracy_val_detailed)
                
        # Return losses
        return losses, losses_cum, losses_val, losses_cum_val, accuracy, accuracy_detailed, accuracy_val, accuracy_val_detailed
=======
                                optimizer, overwrite=True)
                
        # Return losses
        return losses, losses_cum, accuracy, accuracy_val, accuracy_detailed
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546

    def test(self, loss_f, test_dataloader, msg_bot=True):
        if msg_bot == True:
            self.bot.send_msg('Start testing the model..')
        losses = list()
        accuracy = list()
        accuracy_detailed = list()
        total = 0
        losses_cum = 0
<<<<<<< HEAD
        acc = 0
        idxs = 0
        with torch.no_grad():
            for idx, (x, y) in enumerate(test_dataloader):
                x, y = x.to(self.device), y.to(self.device)
                x = self.preprocess(x)
                yhat = self.model(x)
                loss = loss_f(yhat, y.float())
                losses.append([idx+1, loss.item()])
                total += y.size(0)
                losses_cum += loss.item()
                mod_yhat = np.round(yhat.cpu().detach())
                acc += 100 * accuracy_score(y.cpu().detach().numpy(), mod_yhat)
                idxs += 1
                accuracy.append([idx+1, 100 * accuracy_score(y.cpu().detach().numpy(), mod_yhat)])
                accuracy_detailed.extend(list(zip(y.cpu().detach().numpy().tolist(),
                                                  mod_yhat.cpu().detach().numpy().tolist())))
        print('Testset --> Overall Loss: {:.4}.'.format(losses_cum / total))
        print('Accuracy of the model on the test set: %d %%' % (acc / idxs))
        if msg_bot == True:
            self.bot.send_msg('Testset --> Overall Loss: {:.4}.'.format(losses_cum / total))
            self.bot.send_msg('Accuracy of the model on the test set: %d %%' % (acc / idxs))
            
        # Return losses
        return losses, losses_cum, accuracy, accuracy_detailed
=======
        correct = 0
        with torch.no_grad():
            for idx, (x, y) in enumerate(test_dataloader):
                x, y = x.to(self.device), y.to(self.device)
                x = self.replicating_image(x, 3)
                x = self.preprocess(x)
                yhat = self.model(x)
                loss = loss_f(yhat, torch.max(y, 1)[1])
                losses.append([idx+1, loss.item()])
                total += y.size(0)
                losses_cum += loss.item()
                _, mod_yhat = torch.max(yhat, 1)
                _, labels = torch.max(y, 1)
                correct += (mod_yhat == labels).sum().item()
                accuracy.append([idx+1, 100 * (mod_yhat == labels).sum().item() / y.size(0)])
                accuracy_detailed.extend(list(zip(y.cpu().numpy().tolist(),
                                                  yhat.cpu().numpy().tolist())))
        print('Testset --> Overall Loss: {:.4}.'.format(losses_cum / total))
        print('Accuracy of the cnn model on the test set: %d %%' % (
            100 * correct / total))
        if msg_bot == True:
            self.bot.send_msg('Testset --> Overall Loss: {:.4}.'.format(losses_cum / total))
            self.bot.send_msg('Accuracy of the cnn model on the test set: %d %%' % (
            100 * correct / total))
            
        # Return losses
        return losses, accuracy, accuracy_detailed
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546

class ClassificationAgent(Agent):
    r"""An Agent for CNN models."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = TelegramBot(telegram_login)

<<<<<<< HEAD
=======
    def save_state(self, states_path, state_name, optimizer=None, overwrite=False,
                   losses_train=None, losses_cum_train=None, losses_val=None, 
                   losses_cum_val=None, accuracy_train=None, accuracy_det_train=None,
                   accuracy_val=None, accuracy_det_val=None):
        r"""Saves an agent state. Raises an error if the directory exists and 
        overwrite=False. Saves all further results like losses and accuracies as
        .npy files.
        """
        external_save_state(self, states_path, state_name, optimizer, overwrite,
                            losses_train, losses_cum_train, losses_val, losses_cum_val,
                            accuracy_train, accuracy_det_train, accuracy_val, accuracy_det_val)

    def restore_state(self, states_path, state_name, optimizer=None):
        r"""Tries to restore a previous agent state, consisting of a model 
        state and the content of agent_state_dict. Returns whether the restore 
        operation  was successful. Further the results will be loaded as well,
        i.e. losses and accuracies.
        """
        return external_restore_state(self, states_path, state_name, optimizer)

>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
    def train(self, optimizer, loss_f, train_dataloader,
              val_dataloader, nr_epochs=100, start_epoch=0, save_path=None,
              losses=list(), losses_cum=list(), losses_val=list(), losses_cum_val=list(),
              accuracy=list(), accuracy_detailed=list(), accuracy_val=list(),
              accuracy_val_detailed=list(), save_interval=10,
              msg_bot=True, bot_msg_interval=10):
        r"""Train a model through its agent. Performs training epochs, 
        tracks metrics and saves model states.
        """
        assert start_epoch < nr_epochs, 'Start epoch needs to be smaller than the number of epochs!'
        if msg_bot == True:
            self.bot.send_msg('Start training the model for {} epochs..'.format(nr_epochs-start_epoch))
            
        for epoch in range(start_epoch, nr_epochs):
            msg = "Running epoch "
            msg += str(epoch + 1) + " of " + str(nr_epochs) + "."
            print (msg, end = "\r")
            epoch_loss = list()
            results_y = list()
            results_yhat = list()
            total = 0
<<<<<<< HEAD
            acc = 0
            idxs = 0
            for idx, (x, y) in enumerate(train_dataloader):
                x, y = x.to(self.device), y.to(self.device)
                yhat = self.model(x)
                loss = loss_f(yhat, y.float())
                total += y.size(0)
                mod_yhat = np.round(yhat.cpu().detach())
                acc += 100 * accuracy_score(y.cpu().detach().numpy(), mod_yhat)
                idxs += 1
                epoch_loss.append(loss.item())
                results_y.extend(y.cpu().detach().numpy().tolist())
                results_yhat.extend(mod_yhat.cpu().detach().numpy().tolist())
=======
            correct = 0
            for idx, (x, y) in enumerate(train_dataloader):
                x, y = x.to(self.device), y.to(self.device)
                yhat = self.model(x)
                loss = loss_f(yhat, torch.max(y, 1)[1])
                total += y.size(0)
                epoch_loss.append(loss.item())
                _, mod_yhat = torch.max(yhat, 1)
                _, labels = torch.max(y, 1)
                correct += (mod_yhat == labels).sum().item()
                results_y.extend(y.cpu().detach().numpy().tolist())
                results_yhat.extend(yhat.cpu().detach().numpy().tolist())
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            losses.append(epoch_loss)
            losses_cum.append([epoch+1, sum(epoch_loss) / total])
<<<<<<< HEAD
            accuracy.append([epoch+1, acc / idxs])
=======
            accuracy.append([epoch+1, 100 * correct / total])
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            accuracy_detailed.append(list(zip(results_y, results_yhat)))

            # Validate current model based on validation dataloader
            epoch_loss_val = list()
            results_y_val = list()
            results_yhat_val = list()
            results_mod_yhat_val = list()
            total_val = 0
<<<<<<< HEAD
            acc_val = 0
            idxs_val = 0
=======
            correct_val = 0
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            with torch.no_grad():
                for idx, (x, y) in enumerate(val_dataloader):
                    x_val, y_val = x.to(self.device), y.to(self.device)
                    yhat_val = self.model(x_val)
<<<<<<< HEAD
                    loss = loss_f(yhat_val, y_val.float())
                    total_val += y_val.size(0)
                    epoch_loss_val.append(loss.item())
                    mod_yhat_val = np.round(yhat_val.cpu().detach())
                    acc_val += 100 * accuracy_score(y.cpu().detach().numpy(), mod_yhat_val)
                    idxs_val += 1
                    results_y_val.extend(y_val.cpu().detach().numpy().tolist())
                    results_yhat_val.extend(mod_yhat_val.cpu().detach().numpy().tolist())
                losses_val.append(epoch_loss_val)
                losses_cum_val.append([epoch+1, sum(epoch_loss_val) / total_val])
                accuracy_val.append([epoch+1, acc_val / idxs_val])
=======
                    loss = loss_f(yhat_val, torch.max(y_val, 1)[1])
                    total_val += y_val.size(0)
                    epoch_loss_val.append(loss.item())
                    _, mod_yhat_val = torch.max(yhat_val, 1)
                    _, labels_val = torch.max(y_val, 1)
                    correct_val += (mod_yhat_val == labels_val).sum().item()
                    results_y_val.extend(y_val.cpu().detach().numpy().tolist())
                    results_yhat_val.extend(yhat_val.cpu().detach().numpy().tolist())
                losses_val.append(epoch_loss_val)
                losses_cum_val.append([epoch+1, sum(epoch_loss_val) / total_val])
                accuracy_val.append([epoch+1, 100 * correct_val / total_val])
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
                accuracy_val_detailed.append(list(zip(results_y_val, results_yhat_val)))

            print(('Epoch --> Loss --> Accuracy: {} --> {:.4} --> {:.4}%.\n'
                   'Val_Loss --> Val_Accuracy: {:.4} --> {:.4}%.').format(epoch + 1,
                                                    sum(epoch_loss) / total,
<<<<<<< HEAD
                                                    acc / idxs,
                                                    sum(epoch_loss_val) / total_val,
                                                    acc_val / idxs_val))
=======
                                                    100 * correct / total,
                                                    sum(epoch_loss_val) / total_val,
                                                    100 * correct_val / total_val))
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            if (epoch + 1) % bot_msg_interval == 0 and msg_bot:
                self.bot.send_msg(('Epoch --> Loss --> Accuracy: {} --> {:.4} --> {:.4}%.\n'
                                   'Val_Loss --> Val_Accuracy: {:.4} --> {:.4}%.').format(epoch + 1,
                                                                    sum(epoch_loss) / total,
<<<<<<< HEAD
                                                                    acc / idxs,
                                                                    sum(epoch_loss_val) / total_val,
                                                                    acc_val / idxs_val))
=======
                                                                    100 * correct / total,
                                                                    sum(epoch_loss_val) / total_val,
                                                                    100 * correct_val / total_val))
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
            # Save agent and optimizer state
            if (epoch + 1) % save_interval == 0 and save_path is not None:
                print('Saving current state after epoch: {}.'.format(epoch + 1))
                self.save_state(save_path, 'epoch_{}'.format(epoch + 1),
                                optimizer, True, losses, losses_cum, losses_val,
                                losses_cum_val, accuracy, accuracy_detailed, accuracy_val,
                                accuracy_val_detailed)
                
        # Return losses
        return losses, losses_cum, losses_val, losses_cum_val, accuracy, accuracy_detailed, accuracy_val, accuracy_val_detailed

    def test(self, loss_f, test_dataloader, msg_bot=True):
        if msg_bot == True:
            self.bot.send_msg('Start testing the model..')
        losses = list()
        accuracy = list()
        accuracy_detailed = list()
        total = 0
        losses_cum = 0
<<<<<<< HEAD
        acc = 0
        idxs = 0
=======
        correct = 0
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
        with torch.no_grad():
            for idx, (x, y) in enumerate(test_dataloader):
                x, y = x.to(self.device), y.to(self.device)
                yhat = self.model(x)
<<<<<<< HEAD
                loss = loss_f(yhat, y.float())
                losses.append([idx+1, loss.item()])
                total += y.size(0)
                losses_cum += loss.item()
                mod_yhat = np.round(yhat.cpu().detach())
                acc += 100 * accuracy_score(y.cpu().detach().numpy(), mod_yhat)
                idxs += 1
                accuracy.append([idx+1, 100 * accuracy_score(y.cpu().detach().numpy(), mod_yhat)])
                accuracy_detailed.extend(list(zip(y.cpu().detach().numpy().tolist(),
                                                  mod_yhat.cpu().detach().numpy().tolist())))
        print('Testset --> Overall Loss: {:.4}.'.format(losses_cum / total))
        print('Accuracy of the model on the test set: %d %%' % (acc / idxs))
        if msg_bot == True:
            self.bot.send_msg('Testset --> Overall Loss: {:.4}.'.format(losses_cum / total))
            self.bot.send_msg('Accuracy of the model on the test set: %d %%' % (acc / idxs))

=======
                loss = loss_f(yhat, torch.max(y, 1)[1])
                losses.append([idx+1, loss.item()])
                total += y.size(0)
                losses_cum += loss.item()
                _, mod_yhat = torch.max(yhat, 1)
                _, labels = torch.max(y, 1)
                correct += (mod_yhat == labels).sum().item()
                accuracy.append([idx+1, 100 * (mod_yhat == labels).sum().item() / y.size(0)])
                accuracy_detailed.extend(list(zip(y.cpu().numpy().tolist(),
                                                  yhat.cpu().numpy().tolist())))
        print('Testset --> Overall Loss: {:.4}.'.format(losses_cum / total))
        print('Accuracy of the cnn model on the test set: %d %%' % (
            100 * correct / total))
        if msg_bot == True:
            self.bot.send_msg('Testset --> Overall Loss: {:.4}.'.format(losses_cum / total))
            self.bot.send_msg('Accuracy of the cnn model on the test set: %d %%' % (
            100 * correct / total))
            
>>>>>>> 6192c2bfa88c3375ba21cd95f262a03613b79546
        # Return losses
        return losses, losses_cum, accuracy, accuracy_detailed